import json
import logging
import os

from sklearn import preprocessing
from rasa.core.policies.prolog_policy_data import dialog_events_synthesizer
from typing import Optional, Dict, Text, Any, List
from rasa.core.policies.prolog_policy_data.constants import PROLOG_EXTENSION, PROLOG_POLICY_FILE_KEY_NAME_IN_CONFIG, \
    PROLOG_INTERFACE_RULE_NAME, PROLOG_CONSULT_RULE_NAME, PROLOG_RESPONSE_VARIABLE_NAME, \
    PROLOG_POLICY_PENDING_RESPONSES_METADATA_KEY_NAME, PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME, \
    PROLOG_RULES_CODE_PATH_IN_AGENT_DIRECTORY, PROLOG_DIALOG_STRUCTURE_PREPROCESSING_CODE_PATH, DIALOG_EVENTS_KEY_NAME, \
    ACTION_NAME_KEY_NAME, EVENT_NAME_KEY_NAME, USER_EVENT_EVENT_NAME, DISCARDED_ACTION_NAMES_LIST, \
    EVENT_SYNTHESIZER_CLASS_NAME_SUFFIX, PROLOG_DEFAULT_RESPONSE_PREDICATE, INTENT_KEY_NAME, ENTITIES_KEY_NAME
from rasa.core.constants import POLICY_PRIORITY, DEFAULT_POLICY_PRIORITY
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.core.policies.policy import Policy, PolicyPrediction, confidence_scores_for
from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.core.constants import ACTION_LISTEN_NAME
from rasa.shared.core.domain import Domain
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.core.trackers import DialogueStateTracker
from swiplserver import PrologMQI, PrologThread, PrologError
from rasa.core.policies.prolog_policy_data.prolog_processes_cache import prolog_process_cache

logger = logging.getLogger(__name__)


def _get_dialog_data_synthesized(non_synthesized_data):
    reduced_dialog_events = []
    for elem in non_synthesized_data[DIALOG_EVENTS_KEY_NAME]:
        action_name = elem.get(ACTION_NAME_KEY_NAME, None)
        event_name = elem.get(EVENT_NAME_KEY_NAME)
        if event_name == USER_EVENT_EVENT_NAME or action_name and action_name not in DISCARDED_ACTION_NAMES_LIST:
            synthesizer = getattr(dialog_events_synthesizer,
                                  f"{str(elem[EVENT_NAME_KEY_NAME]).capitalize()}{EVENT_SYNTHESIZER_CLASS_NAME_SUFFIX}",
                                  None)
            if synthesizer:
                entities_of_intent = synthesizer().reduce(elem).get("entities", [])
                if entities_of_intent != []:
                    entities_without_rep = []
                    added_entities = []
                    intent_without_rep = {"intent": synthesizer().reduce(elem).get("intent")}
                    for x in entities_of_intent:
                        if not added_entities.__contains__(x[0]):
                            added_entities.append(x[0])
                            entities_without_rep.append(x)
                    intent_without_rep['entities'] = entities_without_rep
                    reduced_dialog_events.append(intent_without_rep)
                else:
                    reduced_dialog_events.append(synthesizer().reduce(elem))

                # print("////////////reduced_dialog_events original")
                # print(synthesizer().reduce(elem))
                # print("////////////reduced_dialog_events modificado")
                # print(reduced_dialog_events)
                # reduced_dialog_events.append(synthesizer().reduce(elem))
    return reduced_dialog_events


def _is_config_prolog_code_path_correct(prolog_code_path: str):
    if not os.path.isabs(prolog_code_path):
        logger.warning(
            f"Como el path ({prolog_code_path}) no es absoluto, su existencia será validada cuando se realicen "
            f"predicciones"
        )
    elif not os.path.exists(prolog_code_path):
        raise FileNotFoundError(f"No se encuentra el archivo {prolog_code_path}")
    return True


def _is_config_prolog_file_correct(config: Dict[Text, Any]):
    prolog_file: str = config.get(PROLOG_POLICY_FILE_KEY_NAME_IN_CONFIG, None)
    if prolog_file is None:
        raise Exception("No se definio un archivo al que realizar consultas en el archivo config.yml")
    elif not prolog_file.endswith(PROLOG_EXTENSION):
        raise Exception("El archivo para PrologPolicy (definido en config.yml) no es un código Prolog")
    return True


def _setup_prolog_thread(prolog_thread: PrologThread, user_prolog_code_path: str):
    preprocessing_code_path_formatted = PROLOG_DIALOG_STRUCTURE_PREPROCESSING_CODE_PATH.replace('\\', '\\\\')
    user_code_path_formatted = user_prolog_code_path.replace('\\', '\\\\')
    prolog_thread.query_async(
        value=f"{PROLOG_CONSULT_RULE_NAME}('{preprocessing_code_path_formatted}')",
        find_all=False
    )
    prolog_thread.query_async(
        value=f"{PROLOG_CONSULT_RULE_NAME}('{user_code_path_formatted}')",
        find_all=False
    )


def _get_prolog_thread(path_to_prolog_code: str):
    hashed_path_to_prolog_code = hash(path_to_prolog_code)
    if hashed_path_to_prolog_code not in prolog_process_cache.keys():
        prolog_thread = PrologMQI().create_thread()
        _setup_prolog_thread(
            prolog_thread=prolog_thread,
            user_prolog_code_path=path_to_prolog_code
        )
        prolog_process_cache[hashed_path_to_prolog_code] = prolog_thread
    return prolog_process_cache[hashed_path_to_prolog_code]


def _try_get_prolog_response(prolog_thread: PrologThread, predicate, arguments):
    try:
        response = prolog_thread.query(
            value=f"{predicate}({arguments},{PROLOG_RESPONSE_VARIABLE_NAME})"
        )
    except PrologError:
        response = False
    return response
    

def _get_prolog_response(prolog_thread: PrologThread, synthesized_data):
    dialog_as_json = json.dumps(synthesized_data).replace("'", "\'")
    intent = synthesized_data[-1][INTENT_KEY_NAME]
    entities = synthesized_data[-1][ENTITIES_KEY_NAME]
    consults = [
        (PROLOG_INTERFACE_RULE_NAME, f"'{dialog_as_json}'"),
        (intent, entities),
        (PROLOG_DEFAULT_RESPONSE_PREDICATE, entities)
    ]

    for consult in consults:
        response = _try_get_prolog_response(
            prolog_thread=prolog_thread,
            predicate=consult[0],
            arguments=consult[1]
        )
        if response: return response


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.POLICY_WITH_END_TO_END_SUPPORT, is_trainable=False
)
class PrologPolicy(Policy):

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            POLICY_PRIORITY: DEFAULT_POLICY_PRIORITY
        }

    @classmethod
    def _metadata_filename(cls) -> Optional[Text]:
        return "PrologPolicy"

    def __init__(
            self,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            featurizer: Optional[TrackerFeaturizer] = None,
    ):
        if not _is_config_prolog_file_correct(config=config) and _is_config_prolog_code_path_correct(
                config[PROLOG_POLICY_FILE_KEY_NAME_IN_CONFIG]):
            raise Exception("La configuracion de Prolog Policy no es correcta, no se puede instanciar la politica")
        super().__init__(
            config=config,
            model_storage=model_storage,
            resource=resource,
            execution_context=execution_context,
            featurizer=featurizer
        )
        self._prolog_policy_path = config[PROLOG_POLICY_FILE_KEY_NAME_IN_CONFIG]
        self._current_conversation_responses = {}

    def _set_agent_relative_prolog_code_path(self, agent_relative_path: str):
        agent_relative_absolute_path = os.path.abspath(agent_relative_path)
        if _is_config_prolog_code_path_correct(agent_relative_absolute_path):
            self._prolog_policy_path = agent_relative_absolute_path
        else:
            raise Exception("El path relativo al agente no es correcto")

    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            **kwargs: Any
    ) -> Resource:
        pass

    def predict_action_probabilities(
            self,
            tracker: DialogueStateTracker,
            domain: Domain,
            rule_only_data: Optional[Dict[Text, Any]] = None,
            **kwargs: Any
    ) -> PolicyPrediction:

        if tracker.sender_id not in self._current_conversation_responses.keys():
            self._current_conversation_responses[tracker.sender_id] = {
                PROLOG_POLICY_PENDING_RESPONSES_METADATA_KEY_NAME: False,
                PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME: []
            }

        logger.debug(f"Current conversation responses {self._current_conversation_responses}")

        if self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_PENDING_RESPONSES_METADATA_KEY_NAME]:
            if len(self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME]) > 0:
                return self._prediction(confidence_scores_for(self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME].pop(0), 1.0, domain))
            else:
                self._current_conversation_responses.pop(tracker.sender_id)
                return self._prediction(confidence_scores_for(ACTION_LISTEN_NAME, 1.0, domain))

        if not os.path.isabs(self._prolog_policy_path):
            from CharlatanAccess import charlatan_manager
            self._set_agent_relative_prolog_code_path(
                os.path.join(
                    charlatan_manager.get_agent_path(tracker.agent_name),
                    PROLOG_RULES_CODE_PATH_IN_AGENT_DIRECTORY,
                    self._prolog_policy_path
                )
            )

        synthesized_data = _get_dialog_data_synthesized(tracker.as_dialogue().as_dict())
        prolog_thread = _get_prolog_thread(self._prolog_policy_path)
        response = _get_prolog_response(prolog_thread, synthesized_data)

        for r in response[0][PROLOG_RESPONSE_VARIABLE_NAME]:
            self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME].append(r)
        self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_PENDING_RESPONSES_METADATA_KEY_NAME] = True
        return self._prediction(confidence_scores_for(self._current_conversation_responses[tracker.sender_id][PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME].pop(0), 1.0, domain))

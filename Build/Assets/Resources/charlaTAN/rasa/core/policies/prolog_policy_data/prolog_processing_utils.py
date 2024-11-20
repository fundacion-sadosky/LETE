import logging
from typing import Dict, List, Text
from CharlatanAccess import charlatan_message_history
from rasa.shared.constants import UTTER_PREFIX
from rasa.core.policies.prolog_policy_data.dialog_events_synthesizer import UserEventDataSynthesizer


logger = logging.getLogger(__name__)

def _map_message(messages: List[Text]) -> Dict:
    result = []
    for message in messages:
        if "utter_name" in message["parse_data"].keys():
            result.append([message["parse_data"]["utter_name"]])
        else:
            synthesized_data = UserEventDataSynthesizer().reduce(message)
            result.append([synthesized_data["intent"], synthesized_data["entities"][0]])
    return result        

def _is_entity_in_real_entities(entity_to_find, real_entities):
    for real_entity in real_entities:
        if real_entity[0] == entity_to_find[0] and real_entity[1] == entity_to_find[1]:
            return True
    return False        

def _matches_intent_and_entities(
        full_history_message_intent: Text, 
        full_history_message_entities: List[Text],
        history_to_match_message_intent: Text,
        history_to_match_message_entities: List[Text]
    ) -> bool:
    if full_history_message_intent != history_to_match_message_intent: return False
    else:
        for entity_to_find in history_to_match_message_entities:
            if not _is_entity_in_real_entities(entity_to_find, full_history_message_entities):
                return False
        return True        


def match_history(conversation_id, history_to_match: List):
    current_full_history = charlatan_message_history.get_messages_of_conversation(id_conversation=conversation_id)

    if len(history_to_match) > len(current_full_history):
        return False
    else:
        current_history_to_compare = _map_message(list(map(lambda single_message : single_message.to_dict(), current_full_history[-(len(history_to_match)):])))     

        for index in range(len(history_to_match)):
            if not history_to_match[index][0].startswith(UTTER_PREFIX):
                if current_history_to_compare[index][0].startswith(UTTER_PREFIX):
                    return False
                elif not _matches_intent_and_entities(
                    full_history_message_intent=current_history_to_compare[index][0], 
                    full_history_message_entities=current_history_to_compare[index][1:],
                    history_to_match_message_intent=history_to_match[index][0],
                    history_to_match_message_entities=history_to_match[index][1:]
                ):
                    return False
            else:
                if history_to_match[index][0] != current_history_to_compare[index][0]:
                    return False
        return True    
  
from rasa.core.policies.prolog_policy_data.constants import (
    ENTITY_NAME_KEY_NAME,
    ENTITY_VALUE_KEY_NAME,
    INTENT_KEY_NAME,
    ENTITIES_KEY_NAME,
    PARSED_DATA_KEY_NAME,
    DATA_NAME_KEY_NAME,
    ACTION_KEY_NAME,
)


def entity_reducer(entity_dict):
    return [
        entity_dict[ENTITY_NAME_KEY_NAME],
        entity_dict[ENTITY_VALUE_KEY_NAME]
    ]


class DialogueEventDataSynthesizer:
    def reduce(self, event_dict):
        pass


class UserEventDataSynthesizer(DialogueEventDataSynthesizer):
    def reduce(self, event_dict):
        return {
            INTENT_KEY_NAME: event_dict[PARSED_DATA_KEY_NAME][INTENT_KEY_NAME][DATA_NAME_KEY_NAME],
            ENTITIES_KEY_NAME: list(map(entity_reducer, event_dict[PARSED_DATA_KEY_NAME][ENTITIES_KEY_NAME])),
        }


class ActionEventDataSynthesizer(DialogueEventDataSynthesizer):
    def reduce(self, event_dict):
        return {
            ACTION_KEY_NAME: event_dict[DATA_NAME_KEY_NAME],
        }

#for dialog_events_synthesizer.py
EVENT_KEY_NAME = "event"
TIMESTAMP_KEY_NAME = "timestamp"
ACTION_KEY_NAME = "action"
PARSED_DATA_KEY_NAME = "parse_data"
INTENT_KEY_NAME = "intent"
TEXT_KEY_NAME = "text"
ENTITIES_KEY_NAME = "entities"
DATA_NAME_KEY_NAME = "name"
ENTITY_NAME_KEY_NAME = "entity"
ENTITY_VALUE_KEY_NAME = "value"

#for prolog_policy.py
DIALOG_EVENTS_KEY_NAME = "events"
EVENT_NAME_KEY_NAME = "event"
ACTION_NAME_KEY_NAME = "name"
USER_EVENT_EVENT_NAME = "user"
DISCARDED_ACTION_NAMES_LIST = ["action_listen", "action_session_start"]
EVENT_SYNTHESIZER_CLASS_NAME_SUFFIX = "EventDataSynthesizer"

PROLOG_EXTENSION = ".pl"
PROLOG_POLICY_FILE_KEY_NAME_IN_CONFIG = "file"
PROLOG_INTERFACE_RULE_NAME = "response"
PROLOG_CONSULT_RULE_NAME = "consult"
PROLOG_RESPONSE_VARIABLE_NAME = 'X'
PROLOG_POLICY_PENDING_RESPONSES_METADATA_KEY_NAME = "pending_responses"
PROLOG_POLICY_RESPONSES_LIST_METADATA_KEY_NAME = "responses_list"
PROLOG_RULES_CODE_PATH_IN_AGENT_DIRECTORY = "data"
PROLOG_DIALOG_STRUCTURE_PREPROCESSING_CODE_PATH = "rasa/core/policies/prolog_policy_data/dialog_structure_preprocessing.pl"
PROLOG_DEFAULT_RESPONSE_PREDICATE = "default"
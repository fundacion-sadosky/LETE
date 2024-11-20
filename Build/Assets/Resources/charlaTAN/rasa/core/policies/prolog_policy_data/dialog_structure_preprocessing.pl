:- use_module(library(http/json)).

response(DIALOG_AS_JSON, UTTERS) :-
    atom_json_dict(DIALOG_AS_JSON,DIALOG_AS_LIST,[]),
    current_story(DIALOG_AS_LIST, [], CURRENT_EVENT_LIST),
    generate_utter(CURRENT_EVENT_LIST, UTTERS).

intent(DIALOG_EVENT_DICT, INTENT) :- get_dict('intent', DIALOG_EVENT_DICT, INTENT).

entities(DIALOG_EVENT_DICT, ENTITIES) :- get_dict('entities', DIALOG_EVENT_DICT, ENTITIES).

action(DIALOG_EVENT_DICT, ACTION) :- get_dict('action', DIALOG_EVENT_DICT, ACTION).

extract_dialog_event(DIALOG_EVENT_DICT, RESULT) :-
    intent(DIALOG_EVENT_DICT, INTENT), entities(DIALOG_EVENT_DICT, ENTITIES), append([[], [INTENT|ENTITIES]], RESULT);
    action(DIALOG_EVENT_DICT, ACTION), append([[], [ACTION]], RESULT).

current_story([], CURRENT_EVENT_LIST, RESULT_LIST) :- RESULT_LIST = CURRENT_EVENT_LIST.
current_story([H|T], CURRENT_EVENT_LIST, RESULT_LIST) :-
    extract_dialog_event(H, DIALOG_EVENT),
    append([CURRENT_EVENT_LIST, [DIALOG_EVENT]], NEW_EVENT_LIST),
    current_story(T,NEW_EVENT_LIST, RESULT_LIST).

generate_utter([H|T], UTTERS) :-
    story([H|T], UTTERS);
    generate_utter(T, UTTERS).
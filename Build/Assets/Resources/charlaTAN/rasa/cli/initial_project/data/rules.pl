story([["greet"],["utter_greet"],["mood_great"]], ["utter_happy"]).
story([["greet"],["utter_greet"],["mood_unhappy"], ["utter_cheer_up"], ["utter_did_that_help"], ["affirm"]], ["utter_happy"]).
story([["greet"],["utter_greet"],["mood_unhappy"], ["utter_cheer_up"], ["utter_did_that_help"], ["deny"]], ["utter_goodbye"]).

greet(_, ["utter_greet"]).
goodbye(_, ["utter_goodbye"]).
affirm(_, ["utter_happy"]).
deny(_, ["utter_goodbye"]).
mood_unhappy(_, ["utter_cheer_up", "utter_did_that_help"]).
bot_challenge(_, ["utter_iamabot"]).
default(_, ["utter_iamabot"]).
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class GetTracker(Action):
    def name(self) -> Text:
        return "get_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # intents_history = []

        # tracker.events contiene todos los eventos desde el inicio del bot
        # for event in tracker.events:
            # los eventos de usuario son los generados al recibir un mensaje
            # if event['event'] == 'user':

                # la lista queda ordenada en orden historico, el primer evento de usuario esta en la posicion 0
                # intents_history.append(event['parse_data']['intent']['name'])

        # intentsText = str(intents_history)
        intentsText = tracker.get_intent_of_latest_message() + "|;"

        for i in tracker.slots:
            if tracker.slots[i] is not None:
                intentsText += i+"|"+str(tracker.slots[i])+"|;"
                print(i+"//"+str(tracker.slots[i]))

        # se devuelve como respuesta de texto la lista de intents historico
        dispatcher.utter_message(text=str(intentsText))

        return []

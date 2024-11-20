from typing import Text, Dict, Any
from conversation.conversation_export import ExportableElement


class ConversationMessage(ExportableElement):
    def __init__(self, id: Text, conversation_id: Text, sender: Text, receiver: Text, text: Text, interpretation: Dict[Text, Any], timestamp: float) -> None:
        self._id = id
        self._conversation_id = conversation_id
        self._sender = sender
        self._receiver = receiver
        self._text = text
        self._interpretation = interpretation
        self._timestamp = float(timestamp)

    def get_id(self) -> Text:
        return self._id

    def get_interpretation(self) -> Dict[Text, Any]:
        return self._interpretation.copy()

    def set_interpretation(self, interpretation: Dict[Text, Any]):
        self._interpretation = interpretation

    def get_conversation_id(self) -> Text:
        return self._conversation_id

    def get_timestamp(self) -> float:
        return self._timestamp

    def __hash__(self) -> int:
        return hash((self._id, self._conversation_id, self._sender, self._receiver))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ConversationMessage):
            return False
        if not self._id == __o._id:
            return False
        if not self._conversation_id == __o._conversation_id:
            return False
        if (self._sender == __o._sender and self._receiver == __o._receiver):
            return self._text == __o._text
        return False

    def to_dict(self) -> Dict[Text, Any]:
        return {
            "id": self._id,
            "conversation_id": self._conversation_id,
            "sender": self._sender,
            "receiver": self._receiver,
            "text": self._text,
            "parse_data": self._interpretation,
            "timestamp": self._timestamp
        }

    def __str__(self) -> str:
        return f"id: {self._id}\n id_conversation: {self._conversation_id}\n sender: {self._sender}\n receiver: {self._receiver}\n text: {self._text}\n interpretation: {self._interpretation}\n timestamp: {self._timestamp}\n"

from typing import Optional, Text, Dict, Any
from conversation.conversation_export import ExportableElement
import time


class ConversationDTO(ExportableElement):
    def __init__(self, id: Optional[Text], participant1: Optional[Text], participant2: Optional[Text], parent_conversation: Optional[Text]) -> None:
        self._id = id
        self._participant1 = participant1
        self._participant2 = participant2
        self._parent_conversation = parent_conversation
        self._timestamp = time.time()

    def get_id(self) -> Text:
        return self._id

    def get_timestamp(self) -> float:
        return self._timestamp

    def get_parent_conversation_id(self) -> Text:
        return self._parent_conversation

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ConversationDTO):
            return False
        if (self._participant1 in (__o._participant1, __o._participant2)) and (self._participant2 in (__o._participant2, __o._participant1)):
            return self._id == __o._id and self._parent_conversation == __o._parent_conversation
        return False

    def __str__(self) -> str:
        return f"id: {self._id} - participant1: {self._participant1} - participant2: {self._participant2} - parent_conversation: {self._parent_conversation}"

    def __hash__(self) -> int:
        return hash((self._parent_conversation, self._participant1, self._participant2))

    def to_dict(self) -> Dict[Text, Any]:
        return {
            "id": self._id,
            "participant1": self._participant1,
            "participant2": self._participant2,
            "parent_conversation": self._parent_conversation,
            "timestamp": self._timestamp
        }

    def is_participant(self, participant_name: Text) -> bool:
        return participant_name in (self._participant1, self._participant2)

    def compare_participant(self, other_to_compare: "ConversationDTO") -> bool:
        return (self._participant1 in (other_to_compare._participant1, other_to_compare._participant2)) and (
            self._participant2 in (other_to_compare._participant2, other_to_compare._participant1))

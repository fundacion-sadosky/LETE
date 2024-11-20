from typing import List, Text
from conversation.conversation_message import ConversationMessage
from conversation.search_criteria.message_criteria import MessageCriteria


class MessageHistory:
    def __init__(self) -> None:
        pass

    def upsert_message(self, new_message: ConversationMessage):
        raise NotImplementedError('Es necesario insertar o updatear un mensaje dado')

    def get_messages_of_conversation(self, id_conversation: Text, search_criteria: MessageCriteria = None) -> List[ConversationMessage]:
        raise NotImplementedError('Es necesario obtener todos los mensajes asociados a una conversacion en particular')

    def get_message_from_id(self, message_id: Text) -> ConversationMessage:
        raise NotImplementedError('Se debe poder obtener un mensaje a partir de su identificador')


class InMemoryMessageHistory(MessageHistory):
    def __init__(self) -> None:
        super().__init__()
        self._log = set()

    def upsert_message(self, new_message: ConversationMessage):
        if new_message in self._log:
            old_interpretation = self.get_message_from_id(new_message.get_id()).get_interpretation()
            old_interpretation.update(new_message.get_interpretation())
            new_message.set_interpretation(old_interpretation)
            self._log.remove(new_message)
        self._log.add(new_message)

    def get_message_from_id(self, message_id: Text) -> ConversationMessage:
        for message in self._log:
            if message.get_id() == message_id:
                return message
        return None

    def get_messages_of_conversation(self, id_conversation: Text, search_criteria: MessageCriteria = None) -> List[ConversationMessage]:
        return sorted(
            list(
                filter(
                    lambda message: message.get_conversation_id() == id_conversation and (search_criteria is None or search_criteria.satisfy(message)),
                    self._log
                )
            ),
            key=lambda e: e.get_timestamp()
        )

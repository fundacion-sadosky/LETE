from conversation.conversation_message import ConversationMessage


class MessageCriteria:
    def satisfy(self, message: ConversationMessage):
        raise NotImplementedError('Debe definir si un mensaje satisface o no el criterio')


class MessageCriteriaTimestampGreater(MessageCriteria):
    def __init__(self, time: float) -> None:
        self._time = time

    def satisfy(self, message: ConversationMessage):
        return message.get_timestamp() > self._time

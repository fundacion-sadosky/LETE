from typing import Text, Any, Dict, Optional, NoReturn
from asyncio import Queue
import uuid
from rasa.core.channels.rest import QueueOutputChannel
from rasa.core.channels.channel import OutputChannel
from CharlatanConstants import UTTER_CUSTOM_METADATA_RECIPIENT_KEY_NAME, NULL_CHATBOT_IN_UTTER_CUSTOM_METADATA
from rasa.core.channels.message_queue import message_queue
from CharlatanAccess import charlatan_message_history, charlatan_conversation_manager
from conversation.conversation_message import ConversationMessage


class MessageRouter(QueueOutputChannel):

    def latest_output(self) -> NoReturn:
        raise NotImplementedError("No se implementa latest_output en MessageRouter")

    @classmethod
    def name(cls) -> Text:
        """Name of MessageRouter."""
        return "MessageRouter"

    def __init__(self, intercept_all: bool, sender_id: Text, agent_name: Text, conversation_id: Text, message_queue: Optional[Queue] = None, message_id: Optional[Text] = None) -> None:
        super().__init__(message_queue)
        self._sender_id = sender_id
        self._intercept_all = intercept_all
        self._agent_name = agent_name
        self._conversation_id = conversation_id
        self._message_id = message_id

    def get_agent_name(self):
        return self._agent_name

    def get_conversation_id(self):
        return self._conversation_id

    def get_message_id(self):
        return self._message_id

    def _enqueue_message(self, recipient: Text, text: Text, id_message, new_conversation_id=None):
        # appends a message into the shared message queue to be processed in the future.
        message_queue.put({
            "sender": self._agent_name,
            "recipient_id": recipient,
            "text": text,
            "conversation_id": new_conversation_id,
            "message_id": id_message
        })

    async def send_response(self, _: Text, message: Dict[Text, Any]) -> None:
        # sends a message through this channel.
        text = message.get("text", None)
        custom = message.get("custom", None)
        timestamp = message.get("timestamp", None)
        utter_name = message.get("utter_action", None)
        custom_recipient = None
        id_message = uuid.uuid4().hex

        if custom:
            custom_recipient = custom.pop(UTTER_CUSTOM_METADATA_RECIPIENT_KEY_NAME)

        if custom_recipient == NULL_CHATBOT_IN_UTTER_CUSTOM_METADATA:
            return
        new_conversation_id = self._conversation_id
        if (custom_recipient or self._intercept_all) and text:
            if custom_recipient:
                new_conversation_id = charlatan_conversation_manager.get_or_create_conversation_id(
                    participant1=self._agent_name,
                    participant2=custom_recipient,
                    parent_conversation=self._conversation_id
                )
            self._enqueue_message(
                recipient=custom_recipient or self._sender_id,
                text=text,
                id_message=id_message,
                new_conversation_id=new_conversation_id
            )
        else:
            await OutputChannel.send_response(self, self._sender_id, message)
        charlatan_message_history.upsert_message(
            ConversationMessage(
                id=id_message,
                conversation_id=new_conversation_id,
                sender=self._agent_name,
                receiver=custom_recipient or self._sender_id,
                text=text,
                interpretation={"utter_name": utter_name},
                timestamp=timestamp
            )
        )

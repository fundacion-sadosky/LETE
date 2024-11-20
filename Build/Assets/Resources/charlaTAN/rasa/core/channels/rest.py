import asyncio
import inspect
import json
import logging
import uuid
from asyncio import Queue, CancelledError
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse, ResponseStream
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn, Union

import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    OutputChannel,
    UserMessage,
)


logger = logging.getLogger(__name__)


class RestInput(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa and
    retrieve responses from the assistant."""

    @classmethod
    def name(cls) -> Text:
        return "rest"

    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[Any]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
        receiver_id: Text,
        collector: OutputChannel
    ) -> None:

        message = UserMessage(
            text, collector, sender_id, input_channel=input_channel, metadata=metadata
        )
        await on_new_message(message, receiver_id)

        await queue.put("DONE")

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get("sender", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req: Request) -> Optional[Text]:
        return req.json.get("message", None)

    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get("input_channel") or self.name()

    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
        return request.json.get("metadata", None)

    def stream_response(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
        receiver_id: Text,
        collector
    ) -> Callable[[Any], Awaitable[None]]:
        async def stream(resp: Any) -> None:
            q: Queue = Queue()
            collector.messages = q
            task = asyncio.ensure_future(
                self.on_message_wrapper(
                    on_new_message=on_new_message,
                    text=text,
                    queue=q,
                    sender_id=sender_id,
                    input_channel=input_channel,
                    metadata=metadata,
                    receiver_id=receiver_id,
                    collector=collector
                )
            )
            while True:
                result = await q.get()
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        """Groups the collection of endpoints used by rest channel."""
        module_type = inspect.getmodule(self)
        if module_type is not None:
            module_name = module_type.__name__
        else:
            module_name = None

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            module_name,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/get_agents", methods=["GET"])
        async def get_agents(request: Request) -> HTTPResponse:
            try:
                from CharlatanAccess import charlatan_manager
                names = []
                for name in charlatan_manager.get_agents().keys():
                    names.append(name)
                return response.json({"agents": names, "code": "OK", "message": "All agent names obtained."})
            except:
                return response.json({"agents": [], "code": "ERR", "message": "Error getting agents."})

        @custom_webhook.route("/register-message", methods=["POST"])
        async def register_message(request: Request) -> Union[ResponseStream, HTTPResponse]:
            from CharlatanAccess import charlatan_manager
            conversation_id = request.args.get("conversation", None)
            agent_name = request.args.get("receiver", None)
            agent = charlatan_manager.get_agent(agent_name)
            agent.register_message_in_conversation(
                text_message=self._extract_message(request),
                sender_id=await self._extract_sender(request),
                conversation_id=conversation_id
            )
            dict_to_export = {"code": "OK", "message": "message recive."}
            return response.json(dict_to_export)

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> Union[ResponseStream, HTTPResponse]:
            receiver_id_from_param = ""
            tupleParams = request.get_query_args()
            dictParams = dict((x, y) for x, y in tupleParams)
            if("receiver" in dictParams):
                receiver_id_from_param = dictParams["receiver"]
            sender_id = await self._extract_sender(request)

            text = self._extract_message(request)
            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)

            if metadata:
                agent_name_from_metadata = metadata.get("agent_name", None)

            from rasa.core.channels.message_router import MessageRouter
            from CharlatanAccess import charlatan_conversation_manager
            conversation_id = charlatan_conversation_manager.get_or_create_conversation_id(
                participant1=sender_id,
                participant2=receiver_id_from_param or agent_name_from_metadata,
                parent_conversation=None
            )
            collector = MessageRouter(
                intercept_all=False,
                agent_name=receiver_id_from_param or agent_name_from_metadata,
                sender_id=sender_id,
                conversation_id=conversation_id,
                message_queue=Queue(),
                message_id=uuid.uuid4().hex
            )

            if should_use_stream:
                # rasa shell
                return response.stream(
                    self.stream_response(
                        on_new_message=on_new_message,
                        text=text,
                        sender_id=sender_id,
                        input_channel=input_channel,
                        metadata=metadata,
                        receiver_id=receiver_id_from_param,
                        collector=collector
                    ),
                    content_type="text/event-stream",
                )
            else:
                # rasa run
                # noinspection PyBroadException
                try:
                    await on_new_message(
                        UserMessage(
                            text,
                            collector,
                            sender_id,
                            input_channel=input_channel,
                            metadata=metadata,
                        ),
                        receiver_id_from_param or agent_name_from_metadata
                    )
                except CancelledError:
                    logger.error(
                        f"Message handling timed out for " f"user message '{text}'."
                    )
                except Exception:
                    logger.exception(
                        f"An exception occured while handling "
                        f"user message '{text}'."
                    )
                aux = []
                tam = collector.messages.qsize()
                for i in range(tam):
                    element = await collector.messages.get()
                    aux.append(element)
                    await collector.messages.put(element)
                return response.json(aux)

        return custom_webhook




class QueueOutputChannel(CollectingOutputChannel):
    """Output channel that collects send messages in a list

    (doesn't send them anywhere, just collects them)."""

    # FIXME: this is breaking Liskov substitution principle
    # and would require some user-facing refactoring to address
    messages: Queue  # type: ignore[assignment]

    @classmethod
    def name(cls) -> Text:
        """Name of QueueOutputChannel."""
        return "queue"

    # noinspection PyMissingConstructor
    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        super().__init__()
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self) -> NoReturn:
        raise NotImplementedError("A queue doesn't allow to peek at messages.")

    async def _persist_message(self, message: Dict[Text, Any]) -> None:
        await self.messages.put(message)

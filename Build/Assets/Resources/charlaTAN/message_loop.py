import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from CharlatanConstants import THREADS_TO_PROCESS_MESSAGES
from rasa.core.channels.message_router import MessageRouter

from rasa.core.channels.message_queue import message_queue

from CharlatanAccess import charlatan_manager

logger = logging.getLogger(__name__)


class MessageLoop(threading.Thread):

    def __init__(self, num=THREADS_TO_PROCESS_MESSAGES):
        super().__init__()
        self._thread_pool = ThreadPoolExecutor(num)
        self._semaphore = threading.Semaphore(num)
        self._message_queue = message_queue

    async def _agent_handles_message(self, message):
        # recipient's agent handles the message in the parameter,
        # the answer must be awaited for the completion of the processing.
        # The semaphore is released at the end.

        # This method must async, because the agents' handle_text method is asynchronous, so
        # the answer must be awaited and an await keyword must be used inside an async method.

        try:
            sender = message.pop("sender")
            recipient = message.pop("recipient_id")
            text = message.pop("text")
            conversation_id = message.pop("conversation_id")
            message_id = message.pop("message_id")
        except KeyError:
            logger.exception("No es posible parsear el mensaje, no existe alguna de las keys del mensaje")
            return
        await asyncio.gather(
            charlatan_manager.get_agent(agent_name=recipient).handle_text(
                text_message=text,
                sender_id=sender,
                output_channel=MessageRouter(
                    intercept_all=True,
                    agent_name=recipient,
                    conversation_id=conversation_id,
                    message_id=message_id,
                    sender_id=sender
                )
            ))
        self._message_queue.task_done()
        self._semaphore.release()

    def _launch_execution(self, args):
        # Passes the responsibility of the message handling to the
        # method _agent_handles_message.
        # This method is necessary because an async method can not be submitted to a ThreadPool,
        # this object must execute not async methods.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._agent_handles_message(args))
        loop.close()

    def close_execution(self):
        # Shutdowns the thread pool for a correct MessageLoop finish.
        self._thread_pool.shutdown(wait=True)
        # To wake up the thread that it is waiting for a queue's object in the run() method
        # it is necessary to put an object into the queue, otherwise, the thread waiting in
        # the run method may not be never woken up.
        message_queue.put(None)

    def run(self):
        # Method that overrides Thread's run method.
        # Gets a message from the message_queue, waiting if it is empty, otherwise
        # acquires a semaphore if it is available and submits the task into the thread pool.
        while True:
            message = self._message_queue.get()
            self._semaphore.acquire()
            try:
                self._thread_pool.submit(self._launch_execution, args=message)
            except RuntimeError:
                return

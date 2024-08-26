import websockets
import asyncio
import logging
import ssl
import os

logger = logging.getLogger(__name__)


class SockeyClient:

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def inbound_queue(self):
        return self._inbound_queue

    @property
    def outbound_queue(self):
        return self._outbound_queue

    @property
    def status(self):
        return self._status

    def __init__(self, ip: str, port: int, token: str):
        self._ip = ip
        self._port = port
        self._token = token
        self._status = "Disconnected"
        self._inbound_queue = asyncio.Queue()
        self._outbound_queue = asyncio.Queue()
        self._exit_queues = asyncio.Event()
        self._handle_queues_task = None

    async def connect(self):
        self._exit_queues.clear()
        self._handle_queues_task = asyncio.create_task(self.handle_queues())
        await self._handle_queues_task

    async def disconnect(self):
        self._exit_queues.set()
        if self._handle_queues_task:  # Ensure that the queue is exited before returning
            await self._handle_queues_task

    async def handle_queues(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        logger.info(os.getcwd())
        ssl_context.load_verify_locations(cafile="resources/auth/server.crt")
        try:  # Can this function be further abstracted?
            async with websockets.connect(
                    f"wss://{self.ip}:{self.port}",
                    ssl=ssl_context,
                    extra_headers={"Authorization": os.getenv("SOCKEY_TOKEN")}  # Catch bad token exceptions!!
            ) as websocket:
                self._status = "Connected"
                logger.info("Websocket connection established!")
                while not self._exit_queues.is_set():
                    # Create tasks for receiving and sending messages
                    receive_task = asyncio.create_task(websocket.recv())
                    send_task = asyncio.create_task(self.outbound_queue.get())
                    exit_task = asyncio.create_task(self._exit_queues.wait())

                    done, pending = await asyncio.wait(
                        [receive_task, send_task, exit_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )

                    if receive_task in done:
                        inbound = receive_task.result()
                        await self.inbound_queue.put(inbound)

                    if send_task in done:
                        outbound = send_task.result()
                        await websocket.send(outbound)

                    if exit_task in done:
                        for task in pending:
                            task.cancel()

                        self._status = "Disconnected"
                        logger.info("Websocket connection closed.")

                        continue

                    # Cancel the pending task to avoid warnings
                    for task in pending:
                        task.cancel()

        except asyncio.CancelledError:
            logger.warning("Websocket listener cancelled! A proper shutdown was passed over!")
        except ConnectionRefusedError:
            logger.error("Connection refused. Is the server running?")

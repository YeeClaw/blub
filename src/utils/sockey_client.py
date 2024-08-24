import websockets
import asyncio
import logging

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

    def __init__(self, ip: str, port: int, inbound_queue: asyncio.Queue, outbound_queue: asyncio.Queue):
        self._ip = ip
        self._port = port
        self.uri = f"ws://{self.ip}:{self.port}"
        self._inbound_queue = inbound_queue
        self._outbound_queue = outbound_queue
        self._status = "Disconnected"

    async def handle_queues(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self._status = "Connected"
                while True:
                    # Create tasks for receiving and sending messages
                    receive_task = asyncio.create_task(websocket.recv())
                    send_task = asyncio.create_task(self.outbound_queue.get())

                    done, pending = await asyncio.wait(
                        [receive_task, send_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )

                    if receive_task in done:
                        inbound = receive_task.result()
                        await self.inbound_queue.put(inbound)

                    if send_task in done:
                        outbound = send_task.result()
                        await websocket.send(outbound)

                    # Cancel the pending task to avoid warnings
                    for task in pending:
                        task.cancel()

        except asyncio.CancelledError:
            logger.info("Websocket listener cancelled.")
        except ConnectionRefusedError:
            logger.error("Connection refused. Is the server running?")

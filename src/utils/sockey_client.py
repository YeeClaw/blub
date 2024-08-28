import websockets
import asyncio
import logging
import ssl

from websockets.exceptions import ConnectionClosedOK

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
        self._exit_socket = asyncio.Event()
        self._start_socket_task = None

    async def connect(self):
        """
        Connect to the websocket server.
        """
        self._exit_socket.clear()
        self._start_socket_task = asyncio.create_task(self.oversee_websocket())
        await self._start_socket_task

    async def disconnect(self):
        """
        Disconnect from the existing websocket connection.
        """
        self._exit_socket.set()
        if self._start_socket_task:  # Ensure that the queue is exited before returning
            await self._start_socket_task

    @staticmethod
    def create_ssl_context():
        """
        Create an SSL context for the websocket connection.
        :return ssl.SSLContext: object
        """
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(cafile="resources/auth/server.crt")
        return ssl_context

    async def oversee_websocket(self) -> None:
        """
        Establishes and manages the websocket client connection.
        """
        uri = f"wss://{self.ip}:{self.port}"
        ssl_context = self.create_ssl_context()
        auth_header = {"Authorization": self._token}
        try:
            async with websockets.connect(uri=uri, ssl=ssl_context, extra_headers=auth_header) as websocket:
                self._status = "Connected"
                logger.info("Websocket connection established!")
                websocket.connection_closed_exc()
                await self.handle_messages(websocket)
        except asyncio.CancelledError:
            logger.warning("Websocket listener cancelled! A proper shutdown was passed over!")
        except ConnectionRefusedError:
            logger.error("Connection refused. Is the server running?")
        except Exception as e:
            logger.error(f"An error occurred in websocket connection: {e}")

    async def handle_messages(self, websocket) -> None:
        """
        Handles the inbound and outbound queues for a websocket connection.
        :param websocket: Websocket object to handle the messages for.
        """
        while not self._exit_socket.is_set():
            # Create tasks for receiving and sending messages
            receive_task = asyncio.create_task(self.receive_message(websocket))
            send_task = asyncio.create_task(self.send_message(websocket))
            exit_task = asyncio.create_task(self._exit_socket.wait())

            done, pending = await asyncio.wait(
                [receive_task, send_task, exit_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            if exit_task in done:
                for task in pending:
                    task.cancel()

                self._status = "Disconnected"
                logger.info("Websocket connection closed.")
                continue

            # Cancel the pending task to avoid warnings
            for task in pending:
                task.cancel()

    async def send_message(self, websocket) -> None:
        """
        Takes a message from the outbound queue and pushes it through the websocket client.
        :param websocket: Websocket client to send the message from.
        """
        outbound = await self.outbound_queue.get()
        await websocket.send(outbound)

    async def receive_message(self, websocket) -> None:
        """
        Receives a message from the websocket client and puts it into the inbound queue.
        :param websocket: Websocket client to receive the message from.
        """
        try:  # Catch in the event that the server closes the connection
            inbound = await websocket.recv()
            await self.inbound_queue.put(inbound)
        except ConnectionClosedOK:
            logger.warning("Tried to listen to a closed socket! Closing client...")
            self._exit_socket.set()
        except Exception as e:
            logger.error(f"An error occurred in receiving message: {e}")
            self._exit_socket.set()

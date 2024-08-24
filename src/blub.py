from discord.ext import commands
import asyncio
import logging

logger = logging.getLogger(__name__)


class Blub(commands.Bot):

    def __init__(self, inbound_queue: asyncio.Queue, outbound_queue: asyncio.Queue, **kwargs):
        super().__init__(**kwargs)
        self.inbound_queue = inbound_queue
        self.outbound_queue = outbound_queue
        self.SOCKET_URI = "ws://127.0.0.1:8080"

    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name}')

        # Load the extensions
        await self.load_extension("commands.mcftb")
        await self.load_extension("commands.utility")

    async def close(self):
        await super().close()
        logger.info("Blub closed!")

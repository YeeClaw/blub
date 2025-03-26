import asyncio
import os
import logging

from discord.ext import commands
from src.utils.sockey_client import SockeyClient

logger = logging.getLogger(__name__)


class Blub(commands.Bot):

    @property
    def sockey_client(self):
        return self._sockey_client

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sockey_client = SockeyClient(
            ip=os.getenv("SOCKEY_IP", ""),
            port=int(os.getenv("SOCKEY_PORT", "")),
            token=os.getenv("SOCKEY_TOKEN", "")
        )

    async def on_ready(self):
        if self.user:
            logger.info(f'Logged in as {self.user.name}')
        else:
            logger.error("User returned null!")

        # Load the extensions
        await self.load_extension("commands.mcftb")
        await self.load_extension("commands.utility")

    async def close(self):
        await super().close()
        if self.sockey_client.status == "Connected":
            await self.sockey_client.disconnect()
            logger.info("Sockey closed!")
        logger.info("Blub closed!")

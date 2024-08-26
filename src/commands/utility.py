import time
import math
import logging
import asyncio
from discord.ext import commands

logger = logging.getLogger(__name__)


async def setup(bot):
    logging.info("Utility commands are loading!")
    await bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        See how fast I am running if I'm running at all!
        """
        start_time = time.time()
        message = await ctx.send("Pinging...")
        end_time = time.time()

        latency = round((end_time - start_time) * 1000)
        if not math.isnan(self.bot.latency):  # In the case of testing.
            bot_latency = round(self.bot.latency * 1000)
        else:
            bot_latency = 0

        await message.edit(content=f"> Pong! 🏓\n> \n> `API Latency: {latency}ms`\n> `Bot Latency: {bot_latency}ms`")

    @commands.command()
    async def start_socket(self, ctx):
        """
        Start the socket connection.
        """
        if ctx.author.id != 190525744907157505:  # Yours truly
            await ctx.send("suck toes")
            return

        if self.bot.sockey_client.status == "Connected":
            await ctx.send("Socket connection is already started!")
        else:
            socket_task = asyncio.create_task(self.bot.sockey_client.connect())
            await ctx.send("Socket connection started!")

    @commands.command()
    async def stop_socket(self, ctx):
        """
        Stop the socket connection.
        """
        if ctx.author.id != 190525744907157505:  # Yours truly
            await ctx.send("suck toes")
            return

        await self.bot.sockey_client.disconnect()
        await ctx.send("Socket connection stopped!")

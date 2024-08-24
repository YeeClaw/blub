import time
import math
import logging
from discord.ext import commands
from mcstatus import JavaServer

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
    async def mcftb(self, ctx, ip: str = ""):
        """
        Gather information on a set minecraft server.
        """
        response = await ctx.send("> Gathering server information...")

        try:
            server = JavaServer.lookup(ip, timeout=5)
            status = server.status()

            await response.edit(
                content=f"\"{status.motd.to_plain()}\"\n> `Current players: {status.players.online}`\n> `Ping : {status.latency:.2f} ms`")
        except TimeoutError:
            await response.edit(content="No server was found")

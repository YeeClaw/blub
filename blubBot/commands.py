import time
import math
from discord.ext import commands
from mcstatus import JavaServer
from private import Private


class PingCommands(commands.Cog):
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
    async def mcftb(self, ctx):
        """
        Gather information on a set minecraft server.
        """
        response = await ctx.send("> Gathering server information...")

        try:
            server = JavaServer.lookup(Private.ip + ":25565", timeout=5)
            status = server.status()

            await response.edit(
                f"\"{status.motd}\"\n> `Current players: {status.players.online}`\n> `Ping : {status.latency:.2f} ms`")
        except TimeoutError:
            await response.edit(content="No server was found")


async def setup(bot):
    await bot.add_cog(PingCommands(bot))

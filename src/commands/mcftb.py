import logging
from discord.ext import commands
from mcstatus import JavaServer

logger = logging.getLogger(__name__)


async def setup(bot):
    logger.info("Mcftb commands are loading!")
    await bot.add_cog(Mcftb(bot))


class Mcftb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, message: str):
        """
        Send a message directly to the game server!
        """
        response = await ctx.send(f"Sending message...\n> {message}")
        await self.bot.outbound_queue.put(f"say {message}")

        server_response = await self.bot.inbound_queue.get()
        if int(server_response) == 1:
            await response.edit(content=f"Message sent!")
        else:
            await response.edit(content=f"Message failed to send!")

    @commands.command()
    async def pingserver(self, ctx, ip: str = ""):
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

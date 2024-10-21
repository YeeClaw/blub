import os
import time
import math
import logging
import asyncio
import psycopg2
from discord.ext import commands

from src.utils.leaderboard_handler import LeaderboardHandler

logger = logging.getLogger(__name__)


async def setup(bot):
    logging.info("Utility commands are loading!")
    await bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
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

        leaderboard = LeaderboardHandler()
        leaderboard.manage_connection()

        get_user_id = f"""
            SELECT user_id
            FROM blub.user
            WHERE discord_id = {ctx.author.id}
            """
        insert_user = f"""
            INSERT INTO blub.user (discord_id)
            VALUES ({ctx.author.id})
            """
        get_discord_id = f"""
            SELECT discord_id
            FROM blub.user
            WHERE user_id = %s
            """

        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
        cursor = conn.cursor()
        cursor.execute(get_user_id)
        current_user = cursor.fetchone()
        if current_user:
            user_id = current_user[0]
        else:
            cursor.execute(insert_user)
            conn.commit()
            cursor.execute(get_user_id)
            final_user = cursor.fetchone()
            user_id = final_user[0]

        if leaderboard.update_highscore(user_id, 1, latency):
            logger.info(f"New highscore for user {user_id} in pingpong!")
            await ctx.send("New highscore! 🎉")
            leaders: list[tuple[int, int]] = leaderboard.generate_leaderboard(1, 3)
            board = "\n"
            for i, (user_id, score) in enumerate(leaders):
                cursor.execute(get_discord_id, (user_id,))
                discord_id = cursor.fetchone()[0]
                board += f"> {i + 1}. {await self.bot.fetch_user(discord_id)}: {score}\n"
            await ctx.send(f"**Leaderboard**\n{board}")

        conn.close()
        cursor.close()
        leaderboard.manage_connection()

    @commands.command()
    async def show_pong(self, ctx: commands.Context):
        """
        Show the current highscores for the ping command.
        """
        leaderboard = LeaderboardHandler()
        leaderboard.manage_connection()

        get_discord_id = f"""
            SELECT discord_id
            FROM blub.user
            WHERE user_id = %s
            """

        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
        cursor = conn.cursor()

        leaders: list[tuple[int, int]] = leaderboard.generate_leaderboard(1, 3)
        board = "\n"
        for i, (user_id, score) in enumerate(leaders):
            cursor.execute(get_discord_id, (user_id,))
            discord_id = cursor.fetchone()[0]
            board += f"> {i + 1}. {await self.bot.fetch_user(discord_id)}: {score}\n"
        await ctx.send(f"**Leaderboard**\n{board}")

        conn.close()
        cursor.close()
        leaderboard.manage_connection()

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

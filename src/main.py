import asyncio
import discord
import logging
import os
import time

from datetime import datetime
from blub import Blub
from src.utils.termination_handler import TerminationHandler

# Initialize logging
os.mkdir("logs") if not os.path.exists("logs") else None
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(f"logs/{datetime.now().date()}.log"),
        logging.StreamHandler()
    ]
)

logging.Formatter.converter = time.gmtime
logger = logging.getLogger(__name__)

# Initialize the bot and the sockey client
intents = discord.Intents.all()  # Fix this (make more precise)
intents.members = True
bot = Blub(command_prefix="!", intents=intents)

# Initialize and register the termination handler
termination_handler = TerminationHandler()
termination_handler.register_terminate_signal()


async def main():
    if not os.getenv("BOT_TOKEN"):
        logger.error("Missing bot token in env!")
        exit()

    bot_task = asyncio.create_task(bot.start(os.getenv("BOT_TOKEN", "")))

    await termination_handler.stop_event.wait()
    logger.info("Termination signal received! Shutting down...")
    await bot.close()
    bot_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())

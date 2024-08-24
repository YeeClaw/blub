import asyncio
import discord
import logging
import os
import time

from datetime import datetime
from dotenv import load_dotenv
from blub import Blub
from src.utils.sockey_client import SockeyClient
from src.utils.termination_handler import TerminationHandler

# Initialize logging
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

# Load environment variables from .env file
if load_dotenv():
    logger.info("Loaded environment variables from .env file!")
else:
    logger.error("Failed to load environment variables from .env file!")

# Establish the inbound and outbound queues
inbound_queue = asyncio.Queue()
outbound_queue = asyncio.Queue()

# Initialize the bot and the sockey client
intents = discord.Intents.all()
intents.members = True
bot = Blub(command_prefix="!", intents=intents, inbound_queue=inbound_queue, outbound_queue=outbound_queue)
sockey_client = SockeyClient(ip="127.0.0.1", port=8080, inbound_queue=inbound_queue, outbound_queue=outbound_queue)

# Initialize and register the termination handler
termination_handler = TerminationHandler()
termination_handler.register_terminate_signal()


async def main():
    bot_task = asyncio.create_task(bot.start(os.getenv("BLUB_TOKEN")))
    sockey_task = asyncio.create_task(sockey_client.handle_queues())

    try:
        await termination_handler.stop_event.wait()
    finally:
        bot_task.cancel()
        sockey_task.cancel()
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

import pytest
import discord
from unittest.mock import AsyncMock
from blub_bot import Blub
from commands import PingCommands


@pytest.mark.asyncio
async def test_ping():
    intents = discord.Intents.all()
    intents.members = True

    bot = Blub("!", intents)
    await bot.load_extension("commands")

    mock_ctx = AsyncMock()
    ping_command = bot.get_command("ping")

    await ping_command.callback(PingCommands(bot), mock_ctx)
    assert mock_ctx.send.call_args[0][0] == "Pinging..."


@pytest.mark.asyncio
async def test_mcftb():
    intents = discord.Intents.all()
    intents.members = True

    bot = Blub("!", intents)
    await bot.load_extension("commands")

    mock_ctx = AsyncMock()
    mcftb_command = bot.get_command("mcftb")

    await mcftb_command.callback(PingCommands(bot), mock_ctx)
    assert mock_ctx.send.call_args[0][0] == "> Gathering server information..."

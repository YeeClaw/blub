import discord
from blub_bot import Blub
from private import Private


def run():
    intents = discord.Intents.all()
    intents.members = True

    bot = Blub("!", intents)  # I think there is a better way to do this with **kwargs. Revisit later.

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

        await bot.load_extension("commands")

    bot.run(token=Private.token)


if __name__ == "__main__":
    run()

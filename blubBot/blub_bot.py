from discord.ext import commands


class Blub(commands.Bot):

    #  There isn't a lot going on here, but in the future this is how I will customize my bot class.

    def __init__(self, prefix, intents):

        super().__init__(command_prefix=prefix, intents=intents)


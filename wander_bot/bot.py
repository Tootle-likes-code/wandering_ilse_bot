import discord
from discord import client
from discord.ext import commands


class WanderingBot(commands.Bot):
    def __init__(self, command_prefix='!', intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!!")

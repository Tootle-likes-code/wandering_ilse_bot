import asyncio

import discord
from discord.ext import commands

from wander_bot.shut_up_cog import ShutUpCog


class WanderingBot(commands.Bot):
    def __init__(self, command_prefix='!', intents=None, default_shut_up_id=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True

        super().__init__(command_prefix=command_prefix, intents=intents)
        asyncio.run(self._add_cogs(default_shut_up_id))

    async def _add_cogs(self, default_shut_up_id):
        await self.add_cog(ShutUpCog(self, default_shut_up_id))

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!!")

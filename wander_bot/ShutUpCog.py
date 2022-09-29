from typing import Optional

import discord
from discord import User, Member
from discord.ext import commands
from discord.ext.commands import Context


class ShutUpCog(commands.Cog):
    def __init__(self, bot: commands.Bot, default_shut_up_id: Optional[int] = None):
        self.bot = bot
        self._default_shut_up_id = default_shut_up_id

    @commands.command("shutup")
    async def shut_up(self, ctx: Context, *, member: str = None):
        member = await self._validate_member(ctx, member)

        message = "Shut Up"
        if member is None:
            message += "!"
        else:
            message += f" <@{member.id}>!!"

        await ctx.send(message)

    async def _validate_member(self, ctx: Context, member: str) -> User | Member:
        if member is not None:
            return discord.utils.get(ctx.guild.members, name=member)
        elif self._default_shut_up_id is not None:
            return await self.bot.fetch_user(self._default_shut_up_id)


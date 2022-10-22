from discord.app_commands import commands
from discord.ext.commands import Context, MissingRequiredArgument

from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesCog(commands.Cog):
    def __init__(self, service: MergeMessagesService):
        self._service = service

    @commands.command(name="watch")
    async def watch_channel(self, ctx: Context):
        self._service.watch_channel(ctx.guild.id, ctx.channel.id)

        await ctx.send(f"Added {ctx.channel.name} to the watch list.")

    @watch_channel.error
    async def watch_channel_error(self, ctx: Context, error: Exception):
        if isinstance(error, TypeError):
            await ctx.send(error.args[0])

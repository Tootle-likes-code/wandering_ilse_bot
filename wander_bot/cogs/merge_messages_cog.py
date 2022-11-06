from discord.ext import commands
from discord.ext.commands import Context

from wander_bot.services.authentication_service import AuthenticationService
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesCog(commands.Cog):
    def __init__(self, merge_service: MergeMessagesService, authentication_services: dict[int, AuthenticationService]):
        self._merge_service = merge_service
        self._authentication_services = authentication_services

    def _authenticate_request(self, ctx: Context) -> bool:
        authentication_service = self._authentication_services.get(ctx.guild.id, None)
        if not authentication_service:
            self._authentication_services[ctx.guild.id] = AuthenticationService(ctx.guild)
            authentication_service = [ctx.guild.id]

        return authentication_service.is_valid_member(ctx.author)

    @commands.command(name="watch")
    async def watch_channel(self, ctx: Context):
        if not self._authenticate_request(ctx):
            await ctx.send("You are not able to add a channel to the watchlist.")

        self._merge_service.watch_channel(ctx.guild.id, ctx.channel.id)

        await ctx.send(f"Added channel '{ctx.channel.name}' to the watch list.")

    @watch_channel.error
    async def watch_channel_error(self, ctx: Context, error: Exception):
        if isinstance(error, TypeError):
            await ctx.send(error.args[0])

    @commands.command(name="stop-watch")
    async def stop_watching_channel(self, ctx: Context):
        if not self._authenticate_request(ctx):
            await ctx.send("You are not able to remove a channel from the watchlist.")

        self._merge_service.watch_channel(ctx.guild.id, ctx.channel.id)

        await ctx.send(f"Removed {ctx.channel.name} from watch list.")

    @stop_watching_channel.error
    async def stop_watch_channel_error(self, ctx: Context, error: Exception):
        if isinstance(error, TypeError):
            await ctx.send(error.args[0])

        if isinstance(error, KeyError):
            await ctx.send(f"Did not have this guild registered to watch anything.")

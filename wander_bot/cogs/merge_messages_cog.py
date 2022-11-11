import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from wander_bot.services.authentication_service import AuthenticationService
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, merge_service: MergeMessagesService,
                 authentication_services: dict[int, AuthenticationService] = None):
        self.bot = bot
        self._merge_service = merge_service
        if authentication_services is None:
            self._authentication_services = {}
        else:
            self._authentication_services = authentication_services

    def _authenticate_request(self, ctx: Context) -> bool:
        authentication_service = self._authentication_services.get(ctx.guild.id, None)
        if not authentication_service:
            self._authentication_services[ctx.guild.id] = AuthenticationService(ctx.guild)
            authentication_service = self._authentication_services.get(ctx.guild.id)

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

    @commands.command(name="get-output")
    async def get_output_channel(self, ctx: Context):
        if not self._authenticate_request(ctx):
            await ctx.send("You don't have permissions to find that out.")

        output_channel = self._merge_service.get_output_channel(ctx.guild.id)
        await ctx.send(f"Current output channel is: {ctx.guild.get_channel(output_channel).name}")

    @get_output_channel.error
    async def get_output_channel_error(self, ctx: Context, error: Exception):
        if isinstance(error, KeyError):
            await ctx.send(f"Did not have this guild registered to watch anything.")

    @commands.command(name="set-output", aliases=['output'])
    async def set_output_channel(self, ctx: Context):
        if not self._authenticate_request(ctx):
            await ctx.send("You do not have permissions to set a channel as the updates channel.")

        self._merge_service.set_output_channel(ctx.guild.id, ctx.channel.id)
        await ctx.send(f"Set '{ctx.channel.name}' as the updates channel.")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        context: commands.Context = await self.bot.get_context(message)
        if context.command is None:
            await self._copy_appropriate_message(message)

    async def _copy_appropriate_message(self, message):
        if not self._merge_service.is_channel_watched(message.guild.id, message.channel.id):
            return

        output_channel_id = self.get_output_channel(message.guild.id)

        if output_channel_id is None:
            return

        output_channel = discord.utils.get(
            message.guild.channels,
            id=self._merge_service.get_output_channel(message.guild.id)
        )
        await output_channel.send(message.content)

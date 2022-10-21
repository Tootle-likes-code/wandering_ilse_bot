from discord.app_commands import commands
from discord.ext.commands import Context

from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesCog(commands.Cog):
    def __init__(self, service: MergeMessagesService):
        self._service = service

    def watch_channel(self, ctx: Context):
        pass

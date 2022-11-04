from discord import Member, Guild, Role

from tests.services.custom_errors.inappropriate_role_error import InappropriateRoleError
from tests.services.custom_errors.no_such_role_error import NoSuchRoleError
from wander_bot.services import guild_config
from wander_bot.services.guild_config import GuildConfig


def _validate_args(guild_id: int, channel_id: int):
    if not isinstance(guild_id, int):
        raise TypeError("Guild ID must be a number.")

    if not isinstance(channel_id, int):
        raise TypeError("Channel ID must be a number.")

class MergeMessagesService:
    def __init__(self):
        self.guild_configs: dict[int, GuildConfig] = {}
        self._load_watched_channels()

    def _load_watched_channels(self):
        pass

    def _validate_user(self, author: Member, owner_id):
        if author.id != owner_id:
            raise InappropriateRoleError()

    def watch_channel(self, guild_id: int, channel_id: int, author: Member, owner_id: int):
        self._validate_user(author, owner_id)
        _validate_args(guild_id, channel_id)

        if guild_id not in self.guild_configs:
            self.guild_configs[guild_id] = guild_config.create_guild_config(guild_id, channel_id)
            return

        self.guild_configs[guild_id].add_channel(channel_id)

    def stop_watching_channel(self, guild_id: int, channel_id: int, author: Member, owner_id: int):
        self._validate_user(author, owner_id)
        _validate_args(guild_id, channel_id)

        try:
            self.guild_configs[guild_id].remove_channel(channel_id)
        except KeyError:
            raise KeyError(f"No Guild with ID '{guild_id}' found.")

    def add_watch_role(self, guild: Guild, role: Role, author: Member):
        if not isinstance(guild, Guild):
            raise TypeError("guild was not of the Guild type.")

        if role not in guild.roles:
            raise NoSuchRoleError(guild, role)

        self._validate_user(author, guild.owner.id)

        self.guild_configs[guild.id].add_watch_role(role)

from wander_bot.services import guild_config
from wander_bot.services.guild_config import GuildConfig


class MergeMessagesService:
    def __init__(self):
        self.guild_configs: dict[int, GuildConfig] = {}
        self._load_watched_channels()

    def _load_watched_channels(self):
        pass

    def watch_channel(self, guild_id: int, channel_id: int):
        if not isinstance(guild_id, int):
            raise TypeError("Guild ID must be a number.")

        if not isinstance(channel_id, int):
            raise TypeError("Channel ID must be a number.")

        if guild_id not in self.guild_configs:
            self.guild_configs[guild_id] = guild_config.create_guild_config(guild_id, channel_id)
            return

        self.guild_configs[guild_id].add_channel(channel_id)

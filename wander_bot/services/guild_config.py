from dataclasses import dataclass, field


@dataclass
class GuildConfig:
    guild_id: int
    watched_channels: set[int] = field(default_factory=set)

    def add_channel(self, channel_id: int) -> None:
        self.watched_channels.add(channel_id)


def create_guild_config(guild_id: int, channel_id: int) -> GuildConfig:
    return GuildConfig(guild_id, {channel_id})


def create_guild_config_with_channels(guild_id: int, channel_ids: list[int]) -> GuildConfig:
    return GuildConfig(guild_id, set(channel_ids))

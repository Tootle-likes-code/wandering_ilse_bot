from dataclasses import dataclass, field


@dataclass
class GuildConfig:
    guild_id: int
    output_channel_id: int | None = None
    watched_channels: set[int] = field(default_factory=set)

    def add_channel(self, channel_id: int) -> None:
        self.watched_channels.add(channel_id)

    def remove_channel(self, channel_id: int) -> None:
        self.watched_channels.discard(channel_id)


def create_guild_config(guild_id: int, channel_id: int = None, output_channel: int = None) -> GuildConfig:
    if channel_id is None:
        return GuildConfig(guild_id, output_channel_id=output_channel)
    return GuildConfig(guild_id, watched_channels={channel_id}, output_channel_id=output_channel)


def create_guild_config_with_channels(guild_id: int, channel_ids: list[int]) -> GuildConfig:
    return GuildConfig(guild_id, watched_channels=set(channel_ids))

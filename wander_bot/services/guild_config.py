from dataclasses import dataclass, field

from discord import Role


@dataclass
class GuildConfig:
    guild_id: int
    watched_channels: set[int] = field(default_factory=set)
    watch_roles: set[Role] = field(default_factory=set)

    def add_channel(self, channel_id: int) -> None:
        self.watched_channels.add(channel_id)

    def remove_channel(self, channel_id: int) -> None:
        self.watched_channels.discard(channel_id)

    def add_watch_role(self, role: Role) -> None:
        self.watch_roles.add(role)

    def remove_watch_role(self, role: Role) -> None:
        self.watch_roles.remove(role)

    def can_add_watch(self, role: Role) -> bool:
        return role in self.watch_roles


def create_guild_config(guild_id: int, channel_id: int) -> GuildConfig:
    return GuildConfig(guild_id, {channel_id})


def create_guild_config_with_channels(guild_id: int, channel_ids: list[int]) -> GuildConfig:
    return GuildConfig(guild_id, set(channel_ids))


def create_guild_config_with_channels_and_roles(guild_id: int, channel_ids: list[int],
                                                roles: list[Role]) -> GuildConfig:
    return GuildConfig(guild_id, set(channel_ids), set(roles))

from discord import Role, Guild


class NoSuchRoleError(Exception):
    def __init__(self, guild: Guild, role: Role):
        self.guild = guild
        self.role = role

    @property
    def message(self):
        return f"The guild '{self.guild.name}' does not have the role '{self.role.name}'."

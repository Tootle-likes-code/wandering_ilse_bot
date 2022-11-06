from discord import Role, Member, Guild

from wander_bot.services.custom_errors.inappropriate_role_error import InappropriateRoleError
from wander_bot.services.custom_errors.no_such_role_error import NoSuchRoleError


class AuthenticationService:
    def __init__(self, guild: Guild, accepted_roles: set() = None):
        self.guild = guild

        if accepted_roles is None:
            self.accepted_roles: set[Role] = set()
        else:
            self.accepted_roles = accepted_roles

    @property
    def owner_id(self) -> int:
        return self.guild.owner_id

    def is_valid_member(self, member: Member) -> bool:
        return member.id == self.owner_id or self._has_valid_roles(member)

    def _has_valid_roles(self, member: Member) -> bool:
        return len(set(member.roles) & set(self.accepted_roles)) > 0

    def add_valid_role(self, role: Role, member: Member) -> None:
        if not self.is_valid_member(member):
            raise InappropriateRoleError()

        if role not in self.guild.roles:
            raise NoSuchRoleError(self.guild, role)

        self.accepted_roles.add(role)

    def remove_valid_role(self, role: Role, member: Member) -> None:
        if not self.is_valid_member(member):
            raise InappropriateRoleError()

        try:
            self.accepted_roles.remove(role)
        except KeyError:
            pass

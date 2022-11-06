import unittest
from unittest.mock import MagicMock, PropertyMock

from wander_bot.services.authentication_service import AuthenticationService
from wander_bot.services.custom_errors.inappropriate_role_error import InappropriateRoleError
from wander_bot.services.custom_errors.no_such_role_error import NoSuchRoleError


class AuthenticationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_role = MagicMock()
        self.invalid_role = MagicMock()
        self.new_role = MagicMock()

        owner_id = 12345
        self.owner_member = MagicMock()
        type(self.owner_member).id = PropertyMock(return_value=owner_id)
        type(self.owner_member).roles = []

        self.valid_role_member = MagicMock()
        type(self.valid_role_member).id = PropertyMock(return_value=23456)
        type(self.valid_role_member).roles = [self.valid_role, self.invalid_role]

        self.invalid_role_member = MagicMock()
        type(self.invalid_role_member).id = PropertyMock(return_value=34567)
        type(self.invalid_role_member).roles = [self.invalid_role]

        self.mock_guild = MagicMock()
        type(self.mock_guild).id = 123
        type(self.mock_guild).owner_id = owner_id
        type(self.mock_guild).roles = {self.valid_role, self.new_role}

        self.test_service = AuthenticationService(self.mock_guild, {self.valid_role})


class InitTests(AuthenticationServiceTests):
    def test_valid_arguments_sets_guild_id(self):
        # Arrange
        expected_result = self.mock_guild

        # Act
        test_service = AuthenticationService(self.mock_guild)

        # Assert
        self.assertEqual(expected_result, test_service.guild)

    def test_valid_arguments_sets_owner_id(self):
        # Arrange
        expected_result = 12345

        # Act
        test_service = AuthenticationService(self.mock_guild)

        # Assert
        self.assertEqual(expected_result, test_service.owner_id)

    def test_valid_arguments_with_no_accepted_roles_initialises_set(self):
        # Arrange
        expected_result = set()

        # Act
        test_service = AuthenticationService(self.mock_guild)

        # Assert
        self.assertEqual(expected_result, test_service.accepted_roles)

    def test_valid_arguments_with_accepted_roles_sets_accepted_roles(self):
        # Arrange
        mock_role = MagicMock()
        expected_result = {mock_role}

        # Act
        test_service = AuthenticationService(self.mock_guild, {mock_role})

        # Assert
        self.assertEqual(expected_result, test_service.accepted_roles)


class IsValidMemberTests(AuthenticationServiceTests):
    def test_member_is_owner_returns_true(self):
        # Act
        result = self.test_service.is_valid_member(self.owner_member)

        # Assert
        self.assertTrue(result)

    def test_member_is_in_valid_role_returns_true(self):
        # Act
        result = self.test_service.is_valid_member(self.valid_role_member)

        # Assert
        self.assertTrue(result)

    def test_member_is_not_owner_and_does_not_have_valid_roles_returns_false(self):
        # Act
        result = self.test_service.is_valid_member(self.invalid_role_member)

        # Assert
        self.assertFalse(result)


class AddValidRoleTests(AuthenticationServiceTests):
    def setUp(self) -> None:
        super().setUp()
        self.invalid_role = MagicMock()

    def test_added_valid_role_using_owner_adds_role(self):
        # Arrange
        expected_result = {self.valid_role, self.new_role}

        # Act
        self.test_service.add_valid_role(self.new_role, self.owner_member)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.accepted_roles)

    def test_added_valid_role_using_valid_role_member_adds_role(self):
        # Arrange
        expected_result = {self.valid_role, self.new_role}

        # Act
        self.test_service.add_valid_role(self.new_role, self.valid_role_member)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.accepted_roles)

    def test_added_valid_role_using_invalid_user_raises_inappropriate_role_error(self):
        # Arrange
        expected_result = {self.valid_role}

        # Act & Assert
        with self.assertRaises(InappropriateRoleError):
            self.test_service.add_valid_role(self.new_role, self.invalid_role_member)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.accepted_roles)

    def test_add_role_not_in_guild_raises_no_such_role_error(self):
        # Assert
        with self.assertRaises(NoSuchRoleError) as ex:
            # Act
            self.test_service.add_valid_role(self.invalid_role, self.owner_member)

        # Assert
        self.assertEqual(self.mock_guild, ex.exception.args[0])
        self.assertEqual(self.invalid_role, ex.exception.args[1])


class RemoveValidRoleTests(AuthenticationServiceTests):
    def test_owner_requests_removal_role_is_removed(self):
        # Arrange
        expected_result = set()

        # Act
        self.test_service.remove_valid_role(self.valid_role, self.owner_member)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.accepted_roles)

    def test_invalid_member_raises_inappropriate_role_error(self):
        # Arrange
        expected_result = {self.valid_role}

        # Assert
        with self.assertRaises(InappropriateRoleError) as ex:
            # Act
            self.test_service.remove_valid_role(self.valid_role, self.invalid_role_member)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.accepted_roles)

    def test_valid_member_removes_role(self):
        # Arrange
        expected_result = set()

        # Act
        self.test_service.remove_valid_role(self.valid_role, self.valid_role_member)

        # Assert
        self.assertEqual(expected_result, self.test_service.accepted_roles)

    def test_valid_member_removes_non_existent_role_does_nothing(self):
        # Arrange
        expected_result = {self.valid_role}

        # Act
        self.test_service.remove_valid_role(self.invalid_role, self.valid_role_member)

        # Assert
        self.assertEqual(expected_result, self.test_service.accepted_roles)


if __name__ == '__main__':
    unittest.main()

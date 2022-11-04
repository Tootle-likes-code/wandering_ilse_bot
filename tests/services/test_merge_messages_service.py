import unittest
from unittest.mock import MagicMock, PropertyMock

from discord import Guild

from wander_bot.cogs.custom_errors.inappropriate_role_error import InappropriateRoleError
from wander_bot.cogs.custom_errors.no_such_role_error import NoSuchRoleError
from wander_bot.services import guild_config
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.default_guild_id = 123
        self.default_channel_id = 456

        self.test_role = MagicMock()
        type(self.test_role).name = PropertyMock(return_value="mocked role")

        self.default_watched_channels = {
            self.default_guild_id: guild_config.create_guild_config_with_channels_and_roles(
                self.default_guild_id,
                [456],
                [self.test_role]
            )
        }
        self.test_owner_id = 12345
        self.default_author = MagicMock()
        type(self.default_author).id = PropertyMock(return_value=self.test_owner_id)
        type(self.default_author).roles = PropertyMock(return_value=[self.test_role])

        self.owner_mock = MagicMock()
        type(self.owner_mock).id = PropertyMock(return_value=self.test_owner_id)

        self.not_authorised_author = MagicMock()
        type(self.not_authorised_author).id = PropertyMock(return_value=456)
        type(self.not_authorised_author).roles = PropertyMock(return_value=[])

        self.test_guild = MagicMock(spec=Guild)
        type(self.test_guild).id = PropertyMock(return_value=self.default_guild_id)
        type(self.test_guild).owner = PropertyMock(return_value=self.owner_mock)
        type(self.test_guild).roles = PropertyMock(return_value=[self.test_role])
        type(self.test_guild).name = PropertyMock(return_value="mocked guild")

        self.test_service = MergeMessagesService()
        self.test_service.guild_configs = self.default_watched_channels


class WatchChannelTests(MergeMessagesServiceTests):
    def test_new_guild_new_channel_adds_guild_and_channel(self):
        # Arrange
        expected_result = {456}
        test_service = MergeMessagesService()

        # Act
        test_service.watch_channel(123, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertSetEqual(expected_result, test_service.guild_configs[123].watched_channels)

    def test_existing_guild_new_channel_adds_channel_to_existing_guild(self):
        # Arrange
        expected_result = {456, 789}

        # Act
        self.test_service.watch_channel(123, 789, self.default_author, self.test_owner_id)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.guild_configs[123].watched_channels)

    def test_existing_guild_existing_channel_does_not_duplicate_existing_channel(self):
        # Arrange
        expected_result = {456}

        # Act
        self.test_service.watch_channel(123, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.guild_configs[123].watched_channels)

    def test_invalid_number_guild_throws_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.watch_channel("hello", 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.watch_channel(123, "world", self.default_author, self.test_owner_id)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_author_is_not_owner_and_invalid_user_returns_inappropriate_role_exception(self):

        # Act
        with self.assertRaises(InappropriateRoleError) as e:
            self.test_service.watch_channel(123, 456, self.not_authorised_author, self.test_owner_id)

    def test_author_is_not_owner_but_is_valid_user_role_adds_channel(self):
        # Arrange
        expected_result = {456, 789}

        # Act
        self.test_service.watch_channel(self.default_guild_id, 789, self.default_author, 9999)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.default_guild_id].watched_channels)


class StopWatchingChannelTests(MergeMessagesServiceTests):
    def test_valid_guild_id_and_channel_id_removes_channel(self):
        # Arrange
        expected_results = set()

        # Act
        self.test_service.stop_watching_channel(123, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertSetEqual(expected_results, self.test_service.guild_configs[123].watched_channels)

    def test_valid_guild_but_no_channel_does_nothing(self):
        # Arrange
        expected_result = self.default_watched_channels

        # Act
        self.test_service.stop_watching_channel(123, 789, self.default_author, self.test_owner_id)

        # Assert
        self.assertDictEqual(expected_result, self.test_service.guild_configs)

    def test_missing_guild_throws_key_error(self):
        # Arrange
        expected_message = "No Guild with ID '456' found."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(KeyError) as ex:
            # Act
            test_service.stop_watching_channel(456, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_guild_throws_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            self.test_service.stop_watching_channel("hello", 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            self.test_service.stop_watching_channel(123, "world", self.default_author, self.test_owner_id)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_author_is_not_owner_throw_inappropriate_role_exception(self):
        # Arrange
        mock_member = MagicMock()
        mock_member.id.return_value = -1

        # Act
        with self.assertRaises(InappropriateRoleError) as e:
            self.test_service.stop_watching_channel(123, 456, mock_member, self.test_owner_id)

    def test_author_is_not_owner_but_is_valid_user_role_adds_channel(self):
        # Arrange
        expected_result = set()

        # Act
        self.test_service.stop_watching_channel(self.default_guild_id, 456, self.default_author, 9999)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.default_guild_id].watched_channels)


class AddWatchRole(MergeMessagesServiceTests):
    def test_valid_guild_from_owner_adds_role(self):
        # Arrange
        expected_result = {self.test_role}

        # Act
        self.test_service.add_watch_role(self.test_guild, self.test_role, self.default_author)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.test_guild.id].watch_roles)

    def test_none_guild_throws_type_error_with_correct_message(self):
        # Arrange
        expected_message = "guild was not of the Guild type."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.add_watch_role(123, self.test_role, self.default_author)

        message = ex.exception.args[0]

        # Assert
        self.assertEqual(expected_message, message)

    def test_guild_not_of_guild_type_raises_type_error(self):
        # Arrange
        expected_message = "guild was not of the Guild type."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.add_watch_role(123, self.test_role, self.default_author)

        message = ex.exception.args[0]

        # Assert
        self.assertEqual(expected_message, message)

    def test_valid_guild_added_by_invalid_user_raises_inappropriate_role_exception(self):
        # Arrange
        type(self.owner_mock).id = PropertyMock(987)

        # Act
        with self.assertRaises(InappropriateRoleError):
            self.test_service.add_watch_role(self.test_guild, self.test_role, self.not_authorised_author)

    def test_add_valid_guild_and_role_again(self):
        # Arrange
        expected_result = {self.test_role}
        self.test_service.guild_configs[self.default_guild_id].watch_roles = {self.test_role}

        # Act
        self.test_service.add_watch_role(self.test_guild, self.test_role, self.default_author)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.test_guild.id].watch_roles)

    def test_guild_does_not_contain_requested_role_raises_NoSuchRoleError(self):
        # Arrange
        expected_message = "The guild 'mocked guild' does not have the role 'mocked role'."
        type(self.test_guild).roles = PropertyMock(return_value=[])

        # Assert
        with self.assertRaises(NoSuchRoleError) as ex:
            # Act
            self.test_service.add_watch_role(self.test_guild, self.test_role, self.default_author)

        message = ex.exception.message

        # Assert
        self.assertEqual(expected_message, message)

    def test_author_is_not_owner_but_is_valid_user_role_adds_channel(self):
        # Arrange
        test_role = MagicMock()
        expected_result = {self.test_role, test_role}

        type(test_role).id = PropertyMock(return_value="456")
        type(self.test_guild).roles = PropertyMock(return_value=[self.test_role, test_role])

        # Act
        self.test_service.add_watch_role(self.test_guild, test_role, self.default_author)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.default_guild_id].watch_roles)


if __name__ == '__main__':
    unittest.main()

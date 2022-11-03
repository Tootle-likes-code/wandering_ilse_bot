import unittest
from unittest.mock import MagicMock, PropertyMock

from tests.services.custom_errors.inappropriate_role_error import InappropriateRoleError
from wander_bot.services import guild_config
from wander_bot.services.guild_config import GuildConfig
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.default_watched_channels = {123: guild_config.create_guild_config(123, 456)}
        self.test_owner_id = 123
        self.default_author = MagicMock()
        type(self.default_author).id = PropertyMock(return_value = self.test_owner_id)


class WatchChannelTests(MergeMessagesServiceTests):
    def test_new_guild_new_channel_adds_guild_and_channel(self):
        # Arrange
        expected_result = self.default_watched_channels
        test_service = MergeMessagesService()

        # Act
        test_service.watch_channel(123, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertDictEqual(expected_result, test_service.guild_configs)

    def test_existing_guild_new_channel_adds_channel_to_existing_guild(self):
        # Arrange
        expected_result = {123: guild_config.create_guild_config_with_channels(123, [456, 789])}
        test_service = MergeMessagesService()
        test_service.guild_configs = self.default_watched_channels

        # Act
        test_service.watch_channel(123, 789, self.default_author, self.test_owner_id)

        # Assert
        self.assertDictEqual(expected_result, test_service.guild_configs)

    def test_existing_guild_existing_channel_does_not_duplicate_existing_channel(self):
        # Arrange
        expected_result = self.default_watched_channels
        test_service = MergeMessagesService()
        test_service.watched_channels = self.default_watched_channels

        # Act
        test_service.watch_channel(123, 456, self.default_author, self.test_owner_id)

        # Assert
        self.assertDictEqual(expected_result, test_service.watched_channels)

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

    def test_author_is_not_owner_returns_inappropriate_role_exception(self):
        # Arrange
        mock_member = MagicMock()
        mock_member.id.return_value = -1
        test_service = MergeMessagesService()

        # Act
        with self.assertRaises(InappropriateRoleError) as e:
            test_service.watch_channel(123, 456, mock_member, self.test_owner_id)

        
        
class StopWatchingChannelTests(MergeMessagesServiceTests):
    def test_valid_guild_id_and_channel_id_removes_channel(self):
        # Arrange
        expected_results = {123: GuildConfig(123)}
        test_service = MergeMessagesService()
        test_service.guild_configs = self.default_watched_channels
        
        # Act
        test_service.stop_watching_channel(123, 456)
        
        # Assert
        self.assertDictEqual(expected_results, test_service.guild_configs)

    def test_valid_guild_but_no_channel_does_nothing(self):
        # Arrange
        expected_result = self.default_watched_channels
        test_service = MergeMessagesService()
        test_service.guild_configs = self.default_watched_channels

        # Act
        test_service.stop_watching_channel(123, 789)

        # Assert
        self.assertDictEqual(expected_result, test_service.guild_configs)

    def test_missing_guild_throws_key_error(self):
        # Arrange
        expected_message = "No Guild with ID '456' found."
        test_service = MergeMessagesService()
        test_service.guild_configs = self.default_watched_channels

        # Assert
        with self.assertRaises(KeyError) as ex:
            # Act
            test_service.stop_watching_channel(456, 456)


        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_guild_throws_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.stop_watching_channel("hello", 456)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.stop_watching_channel(123, "world")

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])




if __name__ == '__main__':
    unittest.main()

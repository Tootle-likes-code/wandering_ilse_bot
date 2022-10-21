import unittest

from wander_bot.services import guild_config
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesServiceTests(unittest.TestCase):
    pass


class WatchChannelTests(MergeMessagesServiceTests):
    def test_new_guild_new_channel_adds_guild_and_channel(self):
        # Arrange
        expected_result = {123: guild_config.create_guild_config(123, 456)}
        test_service = MergeMessagesService()

        # Act
        test_service.watch_channel(123, 456)

        # Assert
        self.assertDictEqual(expected_result, test_service.guild_configs)

    def test_existing_guild_new_channel_adds_channel_to_existing_guild(self):
        # Arrange
        expected_result = {123: guild_config.create_guild_config_with_channels(123, [456, 789])}
        test_service = MergeMessagesService()
        test_service.guild_configs = {123: guild_config.create_guild_config(123, 456)}

        # Act
        test_service.watch_channel(123, 789)

        # Assert
        self.assertDictEqual(expected_result, test_service.guild_configs)

    def test_existing_guild_existing_channel_does_not_duplicate_existing_channel(self):
        # Arrange
        expected_result = {123: {456}}
        test_service = MergeMessagesService()
        test_service.watched_channels = {123: {456}}

        # Act
        test_service.watch_channel(123, 456)

        # Assert
        self.assertDictEqual(expected_result, test_service.watched_channels)

    def test_invalid_number_guild_throws_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.watch_channel("hello", 456)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.watch_channel(123, "world")

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])


if __name__ == '__main__':
    unittest.main()

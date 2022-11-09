import unittest
from unittest.mock import MagicMock, PropertyMock

from discord import Guild

from wander_bot.services import guild_config
from wander_bot.services.merge_messages_service import MergeMessagesService


class MergeMessagesServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.default_guild_id = 123
        self.default_channel_id = 456

        self.default_watched_channels = {
            self.default_guild_id: guild_config.create_guild_config(self.default_guild_id, 456)
        }

        self.test_guild = MagicMock(spec=Guild)
        type(self.test_guild).id = PropertyMock(return_value=self.default_guild_id)
        type(self.test_guild).name = PropertyMock(return_value="mocked guild")

        self.test_service = MergeMessagesService()
        self.test_service.guild_configs = self.default_watched_channels


class WatchChannelTests(MergeMessagesServiceTests):
    def test_new_guild_new_channel_adds_guild_and_channel(self):
        # Arrange
        expected_result = {456}
        test_service = MergeMessagesService()

        # Act
        test_service.watch_channel(123, 456)

        # Assert
        self.assertSetEqual(expected_result, test_service.guild_configs[123].watched_channels)

    def test_existing_guild_new_channel_adds_channel_to_existing_guild(self):
        # Arrange
        expected_result = {456, 789}

        # Act
        self.test_service.watch_channel(123, 789)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.guild_configs[123].watched_channels)

    def test_existing_guild_existing_channel_does_not_duplicate_existing_channel(self):
        # Arrange
        expected_result = {456}

        # Act
        self.test_service.watch_channel(123, 456)

        # Assert
        self.assertSetEqual(expected_result, self.test_service.guild_configs[123].watched_channels)

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


class StopWatchingChannelTests(MergeMessagesServiceTests):
    def test_valid_guild_id_and_channel_id_removes_channel(self):
        # Arrange
        expected_results = set()

        # Act
        self.test_service.stop_watching_channel(123, 456)

        # Assert
        self.assertSetEqual(expected_results, self.test_service.guild_configs[123].watched_channels)

    def test_valid_guild_but_no_channel_does_nothing(self):
        # Arrange
        expected_result = self.default_watched_channels

        # Act
        self.test_service.stop_watching_channel(123, 789)

        # Assert
        self.assertDictEqual(expected_result, self.test_service.guild_configs)

    def test_missing_guild_throws_key_error(self):
        # Arrange
        expected_message = "No Guild with ID '456' found."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(KeyError) as ex:
            # Act
            test_service.stop_watching_channel(456, 456)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_guild_throws_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            self.test_service.stop_watching_channel("hello", 456)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            self.test_service.stop_watching_channel(123, "world")

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_author_is_not_owner_but_is_valid_user_role_adds_channel(self):
        # Arrange
        expected_result = set()

        # Act
        self.test_service.stop_watching_channel(self.default_guild_id, 456)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.default_guild_id].watched_channels)


class SetOutputTests(MergeMessagesServiceTests):
    def test_valid_guild_and_channel_sets_output(self):
        # Arrange
        expected_result = 789

        # Act
        self.test_service.set_output_channel(self.default_guild_id, 789)

        # Assert
        self.assertEqual(expected_result, self.test_service.guild_configs[self.default_guild_id].output_channel_id)

    def test_new_guild_and_valid_channel_adds_guild_sets_output(self):
        # Arrange
        new_guild = 867

        # Act
        self.test_service.set_output_channel(new_guild, 789)

        # Assert
        self.assertTrue(new_guild in self.test_service.guild_configs)

    def test_guild_id_not_a_number_raises_type_error(self):
        # Arrange
        expected_message = "Guild ID must be a number."

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            self.test_service.set_output_channel("hello", 789)

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])

    def test_invalid_number_channel_throws_type_error(self):
        # Arrange
        expected_message = "Channel ID must be a number."
        test_service = MergeMessagesService()

        # Assert
        with self.assertRaises(TypeError) as ex:
            # Act
            test_service.set_output_channel(123, "world")

        # Assert
        self.assertEqual(expected_message, ex.exception.args[0])


class GetOutputChannelTests(MergeMessagesServiceTests):
    def test_returns_output_channel_None_channel(self):
        # Assert
        self.assertIsNone(self.test_service.get_output_channel(self.default_guild_id))

    def test_returns_output_channel_number_channel(self):
        # Arrange
        expected_result = 123
        self.test_service.guild_configs[self.default_guild_id].output_channel_id = 123

        # Act
        result = self.test_service.get_output_channel(self.default_guild_id)

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()

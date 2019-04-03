import time
import unittest
from src.redis_client import RedisCli
from src.settings import RedisConfig


class TestRedisClient(unittest.TestCase):
    @staticmethod
    def get_redis_cli_connection():
        return RedisCli(RedisConfig.SENTINEL_SERVERS,
                        RedisConfig.SENTINEL_MASTER_NAME,
                        RedisConfig.SERVERS_PASSWORD,
                        RedisConfig.SENTINEL_SOCKET_TIMEOUT)

    def save_and_check_key(self, key_name, value):
        """
        Test the saving and reading of a key
        """
        redis_cli = self.get_redis_cli_connection()
        redis_cli.write(key_name, value)
        value_from_server = redis_cli.read(key_name)

        self.assertEqual(value, value_from_server)

    def test_cli_string_input(self):
        """
        Test string input
        """
        self.save_and_check_key('key_str', 'value_key_1')

    def test_cli_tuple_input(self):
        """
        Test dictionary input
        """
        self.save_and_check_key('key_dict', (12,13))

    def test_cli_float_input(self):
        """
        Test float input
        """
        self.save_and_check_key('key_float', 5.9876)

    def test_cli_list_input(self):
        """
        Test list input
        """
        self.save_and_check_key('key_list', [10,45,100])

    def test_cli_int_input(self):
        """
        Test int input
        """
        self.save_and_check_key('key_int', 1000)

    def test_cli_dict_input(self):
        """
        Test dictionary input
        """
        internal_dict = dict(internal_field1=10, internal_field_2='internal string')
        self.save_and_check_key('key_dict', dict(field_1=10,
                                                 field_2=20,
                                                 field_3='test',
                                                 internal_dict=internal_dict))

    def test_cli_bytes_input(self):
        """
        Test bytes input
        """
        self.save_and_check_key('key_bytes', b'123lkdfuh')

    def test_cli_bytearray_input(self):
        """
        Test bytearray input
        """
        self.save_and_check_key('key_bytearray', bytearray('test 123', 'utf8'))

    def test_save_and_wait_expiration_time(self):
        """
        Test if the expiration time is working
        """
        redis_cli = self.get_redis_cli_connection()
        key_name = 'key_expiration_test'
        value = 'value_expiration'
        expiration_seconds = 5
        redis_cli.write(key_name, value, expiration_seconds)
        value_from_server = redis_cli.read(key_name)

        # Check if key was saved successfully
        self.assertEqual(value, value_from_server)

        # Sleep for 1 more second that the expiration time
        time.sleep(expiration_seconds + 1)

        # Read value from server again
        value_from_server = redis_cli.read(key_name)

        # Check if value is now None
        self.assertIsNone(value_from_server)

    def test_delete(self):
        """
        Test if delete is working
        """
        redis_cli = self.get_redis_cli_connection()
        key_name = 'key_delete_test'
        value = 'value_delete_test'

        # save key without expiration time
        redis_cli.write(key_name, value)
        value_from_server = redis_cli.read(key_name)

        # Check if key was saved successfully
        self.assertEqual(value, value_from_server)

        # Delete the key
        self.assertTrue(redis_cli.delete(key_name))

        # Read value from server again
        value_from_server = redis_cli.read(key_name)

        # Check if value is now None
        self.assertIsNone(value_from_server)


if __name__ == '__main__':
    unittest.main()
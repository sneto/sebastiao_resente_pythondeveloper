import unittest
from src.geo_lru import LruClient
from src.redis_client import RedisCli
from src.settings import RedisConfig


class TestLruClient(unittest.TestCase):
    @staticmethod
    def get_redis_cli_connection():
        return RedisCli(RedisConfig.SENTINEL_SERVERS,
                        RedisConfig.SENTINEL_MASTER_NAME,
                        RedisConfig.SERVERS_PASSWORD,
                        RedisConfig.SENTINEL_SOCKET_TIMEOUT)

    def test_is_caching(self):
        """
        Test if a request is being added to the cache
        """
        lru_client = LruClient()
        redis_client = self.get_redis_cli_connection()

        url = 'https://ipinfo.io/json'

        # Start by deleting key from redis (the key will be the entire URL)
        self.assertTrue(redis_client.delete(url))

        # Check if the key doesn't currently exist in cache (the key will be the entire URL)
        redis_result = redis_client.read(url)
        self.assertIsNone(redis_result)

        # Execute request and check if it's result is not None
        request_result = lru_client.request_with_cache(url)
        self.assertIsNotNone(request_result)

        # Read from cache again to check if the value was saved in cache
        redis_result = redis_client.read(url)

        # Redis and request result should be the same
        self.assertEqual(redis_result, request_result)

        # Execute request again, and now it should be returned from cache
        # TODO Assert that request really wasn't executed
        request_result2 = lru_client.request_with_cache(url)
        self.assertEqual(request_result, request_result2)

        # Deleting key from redis
        self.assertTrue(redis_client.delete(url))


if __name__ == '__main__':
    unittest.main()

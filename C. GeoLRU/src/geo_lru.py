import urllib.request
from src.redis_client import RedisCli
from src.settings import RedisConfig


class LruClient:
    """
    Represents the LRU list, linked to reds backends.
    """

    def __init__(self):
        self.redis_client = RedisCli(RedisConfig.SENTINEL_SERVERS,
                                     RedisConfig.SENTINEL_MASTER_NAME,
                                     RedisConfig.SERVERS_PASSWORD,
                                     RedisConfig.SENTINEL_SOCKET_TIMEOUT)

    def request_with_cache(self,
                           url,
                           data=None,
                           headers={},
                           origin_req_host=None,
                           unverifiable=False,
                           method=None,
                           cache_expiration=None):
        """
        Execute a request, but before that, checks if it's value is in cache.
        :param url: Request URL.
        :param data: Request data.
        :param headers: Request headers.
        :param origin_req_host: Request URL.
        :param unverifiable:
        :param method: Request method.
        :param cache_expiration: Time to expire this key in the cache.
        :return:
        """

        # Uses the entire URL as key name
        value_from_cache = self.redis_client.read(url)

        if value_from_cache:
            # TODO renew the key expiration time in the cache
            return value_from_cache

        request = urllib.request.Request(url, data, headers, origin_req_host, unverifiable, method)
        response = urllib.request.urlopen(request)
        response_data = response.read()

        self.redis_client.write(url, response_data, cache_expiration)
        return response_data

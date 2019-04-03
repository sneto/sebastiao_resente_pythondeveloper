# IP info service token (https://ipinfo.io/)
IP_INFO_TOKEN = None


class RedisConfig:
    # Sentinel servers addresses
    SENTINEL_SERVERS = [
        ('', 0)
    ]

    # Sentinel master name
    SENTINEL_MASTER_NAME = 'mymaster'

    # Redis servers password (the master and slaves password must be the same)
    SERVERS_PASSWORD = None

    # Sentinel socket timeout
    SENTINEL_SOCKET_TIMEOUT = 1.0

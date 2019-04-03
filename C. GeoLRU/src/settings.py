# IP info service token (https://ipinfo.io/)
IP_INFO_TOKEN = None


class RedisConfig:
    # Sentinel servers addresses
    SENTINEL_SERVERS = [
        ('142.93.145.2', 26379)
    ]

    # Sentinel master name
    SENTINEL_MASTER_NAME = 'mymaster'

    # Redis servers password (the master and slaves password must be the same)
    SERVERS_PASSWORD = 'onu-2307bc-w987b'

    # Sentinel socket timeout
    SENTINEL_SOCKET_TIMEOUT = 1.0

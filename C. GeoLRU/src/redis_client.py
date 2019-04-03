import json
import geopy.distance
import redis
from redis.sentinel import Sentinel
from src.ipinfo_client import get_ip_location as get_ip_location_ipinfo


class RedisCli:
    def __init__(self, sentinels_addresses, master_name, master_password=None, sentinel_socket_timeout=1.0):
        """
        Create an instance of redis client.
        :param sentinels_addresses: redis sentinel addresses
        :param master_name: redis master name
        :param master_password: redis master password
        :param sentinel_socket_timeout: redis sentinel socket timeout
        """
        self.sentinels_addresses = sentinels_addresses
        self._validate_sentinels_addresses()
        self.master_name = master_name
        self.master_password = master_password
        self.my_location = None
        self.sentinel_socket_timeout = sentinel_socket_timeout
        self._connect()

    @staticmethod
    def _validate_sentinel_address(sentinel_address):
        """
        Validate if a sentinel address is in correct format: (ip: str, port: int)
        :param sentinel_address: Sentinel address dictionary to validade
        :return:
        """
        return sentinel_address is not None and\
               len(sentinel_address) == 2 and\
               isinstance(sentinel_address[0], str) and\
               isinstance(sentinel_address[1], int)

    def _validate_sentinels_addresses(self):
        """
        Validate if the list of sentinel addresses is valid.
        """
        assert isinstance(self.sentinels_addresses, list),\
               'Sentinel addresses must be a list of dictionaries in format (IP, port)'

        sentinel_address_error_message = 'Each sentinel address item must be a list of dictionaries in format' \
                                         ' (IP, port)'

        for sentinel_address in self.sentinels_addresses:
            assert self._validate_sentinel_address(sentinel_address), sentinel_address_error_message

    def _connect(self):
        """
        Connect to the sentinel and load masters and slaves list.
        :return:
        """
        self.sentinel = Sentinel(self.sentinels_addresses, socket_timeout=self.sentinel_socket_timeout)
        self._load_master()
        self._load_slaves()
        self._load_nearest_cache()

    def _redis_server_connection(self, ip, port):
        """
        Return a new instance os redis server connection.
        :param ip: Server IP.
        :param port: Server port.
        :return: A new instance of redis server connection.
        """
        return redis.Redis(
                host=ip,
                port=port,
                password=self.master_password)

    def _load_master(self):
        """
        Communicates with sentinel and load redis master server.
        """
        self.master = None

        try:
            master_info = self.sentinel.discover_master(self.master_name)
        except redis.sentinel.MasterNotFoundError:
            return

        if master_info is not None:
            master_ip, master_port = master_info
            self.master = self._redis_server_connection(master_ip, master_port)

    @staticmethod
    def _get_ip_location(ip=None):
        """
        Get an IP location coordinates.
        :param ip: IP to get coordinates.
        :return: Null if fail or the coordinates if success.
        """
        try:
            return get_ip_location_ipinfo(ip)
        except:
            return None

    def _load_slaves(self):
        """
        Load the slaves list.
        """
        self.slaves = []

        if self.master is None:
            return

        # Load my IP location before loading slaves, so it will be possible to calculate distance
        if self.my_location is None:
            if not self._get_my_location():
                # If my location is unknown, it will not be possible to calculate the nearest slave
                return

        sentinel_slaves = self.sentinel.discover_slaves(self.master_name)
        for slave in sentinel_slaves:
            slave_ip = slave[0]
            # TODO remove
            if slave_ip != '127.0.0.1':
                ip_location = self._get_ip_location(slave[0])
                distance = self.calculate_distance_in_km(ip_location) if ip_location is not None else None
                self.slaves.append(slave + ip_location + (distance,))

    def _get_my_location(self):
        """
        Get the current instance IP location coordinates.
        """
        self.my_location = self._get_ip_location()
        return self.my_location is not None

    def calculate_distance_in_km(self, coordinates):
        """
        Calculate distance from the current IP location and oter coordinates.
        :param coordinates: Coordinates do calculate distance from my location
        :return: The distance between locations.
        """
        return geopy.distance.distance(self.my_location, coordinates).km

    def _load_nearest_cache(self):
        """
        Load the nearest cache server according to the list of slaves.
        """
        self.nearest_cache = None

        # starts with first slave
        nearest_slave = next(iter(self.slaves), None)

        for slave in self.slaves[1:]:
            current_slave_distance = slave[3]
            nearest_slave_distance = nearest_slave[3]
            if nearest_slave_distance is not None and\
                current_slave_distance is not None and\
                nearest_slave_distance > current_slave_distance:
                nearest_slave = slave

        if nearest_slave is not None:
            ip, port = (nearest_slave[0], nearest_slave[1])
            self.nearest_cache = self._redis_server_connection(ip, port)

    @staticmethod
    def _prepare_data_to_write(data):
        """
        Prepara data to write in the server, according to each data type.
        :param data: Data to be prepared
        :return: The data prepared and its type.
        """
        if data is None:
            return data, "none"

        if isinstance(data, bytes):
            return data.decode(), bytes.__name__

        if isinstance(data, bytearray):
            return data.decode('utf8'), bytes.__name__

        return data, data.__class__.__name__

    @staticmethod
    def _decode_writen_data(data, data_type):
        """
        Decode data received from the server during a reding.
        :param data: Data received from the server.
        :param data_type: Original data type of this data before saving in the server.
        :return:
        """
        # Check types that have to be treated in a special way
        if data_type == 'none':
            return None
        if data_type == tuple.__name__:
            return tuple(data)
        if data_type == bytes.__name__:
            return data.encode()
        if data_type == bytearray.__name__:
            return bytearray(data, 'utf8')

        return data

    def _get_object_to_write(self, value):
        """
        Get an object ready to be written in database, composed by two fields: the value itself and its type.
        :param value: Valus do be saved in database.
        :return: an object ready to be written in database, composed by two fields: the value itself and its type.
        """
        encoded_data, type = self._prepare_data_to_write(value)
        return json.dumps(dict(value=encoded_data, type=type))

    def _decode_writen_value(self, writen_value):
        """
        Decode a value received from database, restoring it status according to its original data type.
        :param writen_value: Raw value received from database.
        :return: The value converted to its original status.
        """
        if writen_value is None:
            return None

        decoded_value = writen_value.decode()
        try:
            parsed_value = json.loads(decoded_value)
        except ValueError:
            # This value was not added to cache in the expected json encoded format
            return decoded_value

        return self._decode_writen_data(parsed_value.get('value'), parsed_value.get('type'))

    def read(self, key_name):
        """
        Read a value from the nearest cache server, restoring it data type to the original ones.
        :param key_name: Name of the key to read from server.
        :return: The key value obtained from server, or null if error
        """
        value = None

        if self.nearest_cache is not None:
            value = self._decode_writen_value(self.nearest_cache.get(key_name))

        return value

    def write(self, key_name, value, expiration_seconds=None):
        """
        Write a value in the master database to be replicated to all others.
        :param key_name: Name of the key to be written.
        :param value: Value.
        :param expiration_seconds: Time to expire this key in seconds.
        :return: True: key/value were written | False: error.
        """
        if self.master is not None:
            try:
                self.master.set(key_name, self._get_object_to_write(value), ex=expiration_seconds)
                return True
            except redis.RedisError:
                pass

        return False

    def delete(self, key_name):
        """
        Delete a key from the master database.
        :param key_name: Key to be deleted.
        :return: True: key deleted | False: error.
        """
        if self.master is not None:
            try:
                self.master.delete(key_name)
                return True
            except redis.RedisError:
                pass

        return False

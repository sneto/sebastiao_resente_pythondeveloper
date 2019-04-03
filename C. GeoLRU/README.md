## Geo LRU

I developed a solution using Redis (https://redis.io/) server to persist and synchronize the cache. The goal is to have one Redis master with "N" slaves geographically dispersed connecting to the master server and synchronizing the cache keys. Besides that I used Redis Sentinels (https://redis.io/topics/sentinel) to provide high availability and distribute the master and slaves addresses.

To reduce synchronization conflicts, I'm using the slaves as read only servers and all writes are being done in the master Redis server.

To determine the nearest server, I used IP Info service (https://ipinfo.io/) to get geographical information about the servers and client application IPs, then I compared the distance between each one.

About the integration simplicity, to use it you only have to configure the Sentinel Server information in file "src/settings.py", import "geo_lru.LruClient", create an instance and start using method "src/request_with_cache".

For now I only implemented this method to wrap a cached HTTP request, but using the same idea its possible to implement methods to almost any different source, like files, network sockets, FTP servers, and so on.

To prevent the library user from having to define keys for the cache, I used the own URL as key.

#### Pendences:

I let some TODOs in the source code, but these I consider the most important ones:
- To complete the tests implementation
- To implement options to change from one slave to another in case of fail
- To implement options to reload the slaves server list from time to time, so if new and nearest server are created, the system will automatically start using them

#### Install dependencies

pip install -r requirements.txt


#### Configure (I sent valid configuration data by email)

Configure file src/settings.py

#### Run the tests

python -m unittest discover ./tests/
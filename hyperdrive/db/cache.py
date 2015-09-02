__author__ = 'nmg'

import redis
from redis.exceptions import ConnectionError
import time
import sys

from hyperdrive.common import log as logging

logger = logging.getLogger(__name__)

_SMS_CODE_EXPIRED_SECONDS = 300


class RedisProxy(object):
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connection = None
        self.max_retries = 5
        self.retry_interval = 5

        self.connect()

    def connect(self):
        attempt = 0
        while True:
            attempt += 1
            try:
                self._connect()
                logger.info("Connecting to Redis server on {}:{} succeed".format(self.host, self.port))
                return
            except (ConnectionError, ConnectionRefusedError):
                logger.error("Connecting to Redis failed...retry after {} seconds".format(self.retry_interval))

            if attempt >= self.max_retries:
                logger.error("Connecting to Redis server on {}:{} falied".format(self.host, self.port))
                sys.exit(1)
            time.sleep(self.retry_interval)

    def _connect(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port)
            self.connection = redis.StrictRedis(connection_pool=pool)
        except ConnectionRefusedError:
            raise

    def set(self, key, value, expired=None):
        self.connection.set(key, value, expired if expired else _SMS_CODE_EXPIRED_SECONDS)

    def get(self, key):
        return self.connection.get(key)


if __name__ == '__main__':
    import time
    r = RedisProxy('192.168.99.100', 32775)
    r.set('foo', 'bar', 5)
    print(r.get('foo'))
    time.sleep(6.0)
    print(r.get('foo'))

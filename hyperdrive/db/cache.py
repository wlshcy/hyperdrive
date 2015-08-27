__author__ = 'nmg'

import redis
import time
import sys

from hyperdrive.common import log as logging

logger = logging.getLogger(__name__)

class RedisProxy(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
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
            except ConnectionFailure:
                logger.error("Connecting to Redis failed...retry after {} seconds".format(self.retry_interval))

            if attempt >= self.max_retries:
                logger.error("Connecting to Redis server on {}:{} falied".format(self.host, self.port))
                sys.exit(1)
            time.sleep(self.retry_interval)

    def _connect(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.connection = redis.StrictRedis(connection_pool=pool)

    def set(self, key, value):
        self.connection.set(key, value)

    def get(self, key):
        return self.connection.get(key)
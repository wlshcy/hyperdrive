"""Base Class"""

import eventlet

from hyperdrive import db
from hyperdrive.db.cache import RedisProxy
from hyperdrive.common import cfg


CONF = cfg.CONF

class Base(object):
    def __init__(self):
        self.db = db.API()
        self.cache = RedisProxy(CONF.redis_host, CONF.redis_port)

    def run_task(func, *args):
        """Generate a greenthread to run the `func` with the `args`"""
        eventlet.spawn_n(func, *args)

from hyperdrive.db.mongodb import MongoAPI
from hyperdrive.common import cfg

CONF = cfg.CONF


class API(MongoAPI):
    def __init__(self):

        super(API, self).__init__(CONF.mongo_host,
                                  CONF.mongo_port,
                                  CONF.mongo_db)

    def __getattr__(self, item):
        return getattr(self, item)

from hyperdrive.db.mongodb import MongoAPI
from hyperdrive.common import cfg

conf = cfg.CONF


class API(MongoAPI):
    def __init__(self):

        super(API, self).__init__(conf.mongo_host,
                                  conf.mongo_port,
                                  conf.mongo_db)

    def __getattr__(self, item):
        return getattr(self, item)

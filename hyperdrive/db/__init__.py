from hyperdrive.db.mongodb import MongoAPI
from hyperdrive.common import cfg
from hyperdrive.common import log as logging

conf = cfg.CONF
logger = logging.getLogger(__name__)


class API(MongoAPI):
    def __init__(self):

        self._mongo = MongoAPI(conf.mongo_host,
                               conf.mongo_port,
                               conf.mongo_db)

    def __getattr__(self, method):
        try:
            return getattr(self._mongo, method)
        except AttributeError as exc:
            logger.error(exc)
            raise

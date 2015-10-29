__author__ = 'nmg'


from hyperdrive.base import Base
from hyperdrive import wsgi
from hyperdrive.common.response import Response
import random
from hyperdrive.common import log as logging
import time

logger = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def create(self, req):
        """
        Generate sms code.
        """
        mobile = req.POST['mobile']

        code = '%06d' % random.randint(0, 999999)
        content = code
        try:
            self.sms(mobile, content)
            logger.info('send sms: %s, %s' % (mobile, content))
        except Exception as e:
            logger.error('send sms failed: %s, %s, %s' % (mobile, content, e))

        self.cache.set(mobile, {'code': code, 'time': round(time.time())}, 5)

        return Response(201)


def create_resource():
    return wsgi.Resource(Controller())
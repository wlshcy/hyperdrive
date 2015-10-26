__author__ = 'nmg'


from hyperdrive.base import Base
from hyperdrive import wsgi
from hyperdrive.common.response import HttpResponse
import random


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def create(self, req, body):
        """
        Generate sms code.
        """
        mobile = body.pop('mobile')

        code = '%06d' % random.randint(0, 999999)
        content = code
        try:
            self.sms(mobile, content)
            log.info('send sms: %s, %s' % (mobile, content))
        except Exception as e:
            log.error('send sms failed: %s, %s, %s' % (mobile, content, e))

        self.cache.set(mobile, {'code': code, 'time': round(time.time())}, 5)
        return HttpResponse({"token": body['account']+body['password']})


def create_resource():
    return wsgi.Resource(Controller())
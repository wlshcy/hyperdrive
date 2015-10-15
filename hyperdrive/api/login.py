__author__ = 'nmg'

from hyperdrive.base import Base
from hyperdrive import wsgi
from hyperdrive.common.response import HttpResponse
from hyperdrive.common import utils


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def login(self, req, body):
        """User auth"""
        mobile = body.pop('mobile')
        password = body.pop('password')

        user = self.db.get_user(mobile)
        if not user:
            return HttpResponse({'code': 404, 'message': 'no such user'})

        hashed_password = user['password']
        if not utils.check_password(hashed_password, password):
            return HttpResponse({'code': 403, 'message': 'password is wrong'})

        token = utils.generate_token(str(user['_id']))

        return HttpResponse({"token": token})


def create_resource():
    return wsgi.Resource(Controller())

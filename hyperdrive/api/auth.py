__author__ = 'nmg'

from hyperdrive.base import Base
from hyperdrive import wsgi
from hyperdrive.common.response import HttpResponse


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def create(self, req, body):
        return HttpResponse({"token": body['account']+body['password']})


def create_resource():
    return wsgi.Resource(Controller())
__author__ = 'nmg'

# import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base
from hyperdrive.common import utils
import time
import webob.exc
import os

# from hyperdrive.common.exception import Fault

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all users

        This method returns a dictionary list and each dict contains the following keys:
            - id
            - mobile
        If no user found, empty list will be returned.
        """
        users = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_users()

        for query in queries:
            user = {
                'id': str(query['_id']),
                'mobile': query['mobile'],
                'created': query['created'],
            }
            users.append(user)

        return HttpResponse(users)

    def show(self, req, id):
        """
        Show the user info according to user's id `id`.
        """
        raise NotImplementedError

    def create(self, req, body=None):
        """
        Creating new user. body should contains the following params:

            - mobile     the cell phone number of the user
            - password   the password of the user
            - code       the sms-code has send to user
        """
        try:
            mobile = body.pop('mobile')
            password = body.pop('password')
            # code = body.pop('code')
        except KeyError:
            return webob.exc.HTTPBadRequest()

        # if check_exists(mobile):
        #     return
        #
        # if not check_code(code):
        #     return

        password = self.encrypt_password(password)

        created = round(time.time() * 1000)
        # __id__ = uuid.uuid4().hex

        user = {'mobile': mobile,
                'password': password,
                'created': created}

        # FIXME(nmg): should catch exception if any
        self.db.add_user(user)

        return Response(201)

    def delete(self, req, id):
        """
        Delete user according user `id`
        """
        # FIXME(nmg): should catch exception if any
        return NotImplementedError

    def update(self, req, id, body):
        """Updated user information"""
        return NotImplementedError

    def check_exists(self, mobile):
        """
        Checking if the user has already register
        @param mobile: the cell phone number to be checked
        @return: True or False
        """
        return True if self.db.get_user(mobile) else False

    @staticmethod
    def encrypt_password(password):
        """
        Encrypt password with md5.
        @param password:
        @return: the encrypted password
        """

        return utils.encrypt_password(password)

    def check_code(self, mobile, code):
        """
        Check if the sms code is valid, if not return False, otherwise return True.
        @param code:
        @return: True or False
        """
        cached_code = self.cache.get(mobile)
        return cached_code == code


def create_resource():
    return wsgi.Resource(Controller())
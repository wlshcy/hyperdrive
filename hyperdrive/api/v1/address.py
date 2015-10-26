import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base
import time
import webob.exc
from hyperdrive.common.exception import Fault
import jwt

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all addresses
        
        This method returns a dictionary list and each dict contains the following keys:
            - id 
            - name 
            - mobile
            - address
            - created
        If no item found, empty list will be returned.
        """
        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            payload = jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        uid = payload['uid']

        addresses = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_addresses(uid)

        for query in queries:
            address = {
                'id': str(query['_id']),
                'name': query['name'],
                'mobile': query['mobile'],
                'address': query['address'],
                'created': query['created'],
            }
            addresses.append(address)

        return HttpResponse(addresses)

    def show(self, req, id):
        """
        Show the address info according to item's id `id`.

        This method returns a dictionary with the following keys:
            - id
            - name
            - mobile
            - address
            - created
        If no item found, 404 will returned.
        """
        # FIXME(nmg): should catch exception if any
        query = self.db.get_address(id)

        if not query:
            return Fault(webob.exc.HTTPNotFound())

        address = {
            'id': str(query['_id']),
            'name': query['name'],
            'mobile': query['mobile'],
            'address': query['address'],
            'created': query['created'],
        }

        return HttpResponse(address)

    def create(self, req, body):
        """
        For creating address, body should not be None and
        should contains the following params:
            - name        the name of the user
            - mobile         the mobile of the user
            - address       the address of the user
        """
        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            payload = jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        uid = payload['uid']

        try:
            name = body.pop('name')
            mobile = body.pop('mobile')
            address = body.pop('address')
        except KeyError:
            return webob.exc.HTTPBadRequest()

        created = round(time.time() * 1000)

        address = {
            'uid': uid,
            'name': name,
            'mobile': mobile,
            'address': address,
            'created': created
            }

        # FIXME(nmg): should catch exception if any
        self.db.add_address(address)

        return Response(201)

    def delete(self, req, id):
        """
        delete address according to address id `id`
        """
        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        # FIXME(nmg): should catch exception if any
        self.db.delete_address(id)

        return Response(201)

    def update(self, req, id, body):
        """Updated address information"""

        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        # FIXME(nmg): should catch exception if any
        self.db.update_address(id, body)

        return Response(200)


def create_resource():
    return wsgi.Resource(Controller())

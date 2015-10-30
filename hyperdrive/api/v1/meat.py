from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base

import webob.exc
from hyperdrive.common.exception import Fault

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all meat
        
        This method returns a dictionary list and each dict contains the following keys:
            - id
            - name 
            - img 
            - price 
            - size
        If no meat found, empty list will be returned.
        """

        meats = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_meat()

        for query in queries:
            meat = {
                'id': str(query['_id']),
                'name': query['name'],
                'img': query['img'],
                'price': query['price'],
                'size': query['size']
            }
            meats.append(meat)

        return HttpResponse(meats)

    def show(self, req, id):
        """
        Show the meat info according to meat's id.

        This method returns a dictionary with the following keys:
            - id
            - name
            - img
            - price
            - size
            - origin
            - desc
        If no meat found, 404 will returned.
        """
        # FIXME(nmg): should catch exception if any
        query = self.db.get_meat(id)

        if not query:
            return Fault(webob.exc.HTTPNotFound())

        meat = {
            'id': str(query['_id']),
            'name': query['name'],
            'img': query['img'],
            'price': query['price'],
            'size': query['size'],
            'origin': query['origin'],
            'desc': query['desc']
        }

        return HttpResponse(meat)

    def create(self, req, body=None):
        """
        This operation should be done from management backend.
        """
        raise NotImplementedError()

    def delete(self, req, id):
        """
        This operation should be done from management backend.
        """
        raise NotImplementedError()

    def update(self, req, id, body):
        """
        This operation should be done from management backend.
        """
        raise NotImplementedError()


def create_resource():
    return wsgi.Resource(Controller())

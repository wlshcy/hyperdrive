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
        List all fruits
        
        This method returns a dictionary list and each dict contains the following keys:
            - id 
            - name 
            - img 
            - price 
            - size
        If no fruit found, empty list will be returned.
        """

        fruits = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_fruits()

        for query in queries:
            fruit = {
                'id': str(query['_id']),
                # 'id': query['id'],
                'name': query['name'],
                'img': query['img'],
                'price': query['price'],
                'size': query['size']
            }
            fruits.append(fruit)

        return HttpResponse(fruits)

    def show(self, req, id):
        """
        Show the fruit info according to fruit's id `id`.

        This method returns a dictionary with the following keys:
            - id
            - name
            - img
            - price
            - size
            - origin
            - desc
        If no item found, 404 will returned.
        """
        # FIXME(nmg): should catch exception if any
        query = self.db.get_fruit(id)

        if not query:
            return Fault(webob.exc.HTTPNotFound())

        fruit = {
            'id': str(query['_id']),
            'name': query['name'],
            'img': query['img'],
            'price': query['price'],
            'size': query['size'],
            'origin': query['origin'],
            'desc': query['desc']
        }

        return HttpResponse(fruit)

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

import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base
import time
import webob.exc
from hyperdrive.common.exception import Fault

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all items 
        
        This method returns a dictionary list and each dict contains the following keys:
            - id 
            - name 
            - img 
            - price 
            - size
        If no item found, empty list will be returned.
        """

        items = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_items()

        for query in queries:
            item = {
                'id': str(query['_id']),
                # 'id': query['id'],
                'name': query['name'],
                'img': query['img'],
                'price': query['price'],
                'size': query['size']
            }
            items.append(item)

        return HttpResponse(items)

    def show(self, req, id):
        """
        Show the item info according to item's id `id`.

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
        query = self.db.get_item(id)

        if not query:
            return Fault(webob.exc.HTTPNotFound())

        item = {
            'id': str(query['_id']),
            'name': query['name'],
            'img': query['img'],
            'price': query['price'],
            'size': query['size'],
            'origin': query['origin'],
            'desc': query['desc']
        }

        return HttpResponse(item)

    def create(self, req, body=None):
        """
        For creating item, body should not be None and
        should contains the following params:
            - name        the name of the item
            - img         the image's of the item
            - price       the price of the item
            - size        the size of the item
            - origin      the origin of the item
            - desc        short description
        """
        # id = uuid.uuid4().hex
        name = body.pop('name')
        img = body.pop('img')
        price = body.pop('price')
        size = body.pop('size')
        origin = body.pop('origin')
        desc = body.pop('desc')
        created = round(time.time() * 1000)

        item = {
            'name': name,
            'img': img,
            'price': price,
            'size': size,
            'origin': origin,
            'desc': desc,
            'created': created
            }

        # FIXME(nmg): should catch exception if any
        self.db.add_item(item)

        return Response(201)

    def delete(self, req, id):
        """
        delete item according to item id `id`
        """
        # FIXME(nmg): should catch exception if any
        self.db.delete_item(id)

        return Response(201)

    def update(self, req, id, body):
        """Updated container information"""

        # FIXME(nmg): should catch exception if any
        self.db.update_item(id, body)

        return Response(200)


def create_resource():
    return wsgi.Resource(Controller())

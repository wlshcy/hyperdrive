__author__ = 'nmg'

import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base
import time

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
            - number
            - price
            - address
            - status
            - payed
            - weight
            - created
        If no item found, empty list will be returned.
        """

        orders = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_orders()

        for query in queries:
            item = {
                'id': query['id'],
                'number': query['number'],
                'img': query['img'],
                'price': query['price'],
                'status': query['status'],
                'payed': query['payed'],
                'weight': query['weight'],
                'created': query['created']
            }
            orders.append(item)

        return HttpResponse(orders)

    def show(self, req, id):
        """
        Show the item info according to item's id `id`.

        This method returns a dictionary with following keys:
            - number
            - items
            - price
            - address
            - created
            - status
            - payed
        If no item found, empty dictionary will returned.
        """

        order = {}

        # FIXME(nmg): should catch exception if any
        query = self.db.get_order(id)

        if query is not None:
            order = {
                'number': query['number'],
                'items': query['items'],
                'price': query['price'],
                'address': query['address'],
                'created': query['created'],
                'status': query['status'],
                'payed': query['payed']
            }

        return HttpResponse(order)

    def create(self, req, body=None):
        """
        For creating item, body should not be None and
        should contains the following params:
            - name        the name of the item
            - img         the image's of the item
            - price       the price of the item
            - size        the size of the item
            - origin      the origin of the item
        """
        id = uuid.uuid4().hex
        name = body.pop('name')
        img = body.pop('img')
        price = body.pop('price')
        size = body.pop('size')
        origin = body.pop('origin')
        desc = body.pop('desc')
        created = round(time.time() * 1000)

        item = {'id': id,
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

        return Response(201)


def create_resource():
    return wsgi.Resource(Controller())

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
        List all combos 
        
        This method returns a dictionary list and each dict contains the following keys:
            - _id
            - name 
            - freq 
            - num 
            - price
        If no combos found, empty list will be returned.
        """
	length = req.GET.get('length', 1)
        lastid = req.GET.get('lastid', 0)
	

        combos = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_combos(lastid, length)

        for query in queries:
            item = {
                'id': str(query['_id']),
                'name': query['name'],
                'freq': query['photo'],
                'num': query['price'],
                'price': query['mprice'],
            }
            combos.append(item)

        return HttpResponse(combos)

    def show(self, req, id):
        """
        Show the vegetable info according to vegetables's id.

        This method returns a dictionary with the following keys:
            - _id
            - name
            - img
            - price
            - size
            - origin
            - desc
        If no vegetables found, 404 will returned.
        """
        # FIXME(nmg): should catch exception if any
        query = self.db.get_veg(id)
        LOG.info(query)

        if not query:
            return Fault(webob.exc.HTTPNotFound())

        item = {
            'id': str(query['_id']),
            'name': query['name'],
            'photo': query['photo'],
            'price': query['price'],
            'mprice': query['mprice'],
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
        # # id = uuid.uuid4().hex
        # name = body.pop('name')
        # img = body.pop('img')
        # price = body.pop('price')
        # size = body.pop('size')
        # origin = body.pop('origin')
        # desc = body.pop('desc')
        # created = round(time.time() * 1000)
        #
        # item = {
        #     'name': name,
        #     'img': img,
        #     'price': price,
        #     'size': size,
        #     'origin': origin,
        #     'desc': desc,
        #     'created': created
        #     }
        #
        # # FIXME(nmg): should catch exception if any
        # self.db.add_item(item)
        #
        # return Response(201)
        raise NotImplementedError()

    def delete(self, req, id):
        """
        delete item according to item id `id`
        """
        # FIXME(nmg): should catch exception if any
        # self.db.delete_item(id)
        #
        # return Response(201)
        raise NotImplementedError()

    def update(self, req, id, body):
        """Updated container information"""

        # FIXME(nmg): should catch exception if any
        # self.db.update_item(id, body)
        #
        # return Response(200)
        raise NotImplementedError()

    def slides(self, req):
        """
        List all vegetable slides
        
        This method returns a dictionary list and each dict contains the following keys:
            - _id
            - name 
            - photo 
            - price 
            - mprice
            - size
        If no vegetables found, empty list will be returned.
        """
	length = req.GET.get('length', 10)
	

        slides = []

        # FIXME(nmg): should catch exception if any
        queries = self.db.get_veg_slides()

        for query in queries:
            item = {
                'id': str(query['_id']),
                'name': query['name'],
                'photo': query['photo'],
                'price': query['price'],
                'mprice': query['mprice'],
                'size': query['size']
            }
            slides.append(item)

        return HttpResponse(slides)


def create_resource():
    return wsgi.Resource(Controller())

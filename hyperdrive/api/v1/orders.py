__author__ = 'nmg'

import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.common import utils
from hyperdrive.base import Base
import time
import webob.exc
import jwt

CONF = cfg.CONF

logger = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all orders

        This method returns a dictionary list and each dict contains the following keys:
            - id
            - number
            - price
            - address
            - status
            - weight
            - created
        If no order found, empty list will be returned.
        """
        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            payload = jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        lastid = req.GET['lastid']
        length = req.GET['length']
        user_id = payload['id']

        orders = []

        # FIXME(nmg): should catch all exception if any
        try:
            queries = self.db.get_orders(user_id, lastid, length)
        except AttributeError:
            return webob.exc.HTTPInternalServerError()

        for query in queries:
            item = {
                'id': query['id'],
                'number': query['number'],
                'img': query['img'],
                'price': query['price'],
                'status': query['status'],
                'weight': query['weight'],
                'created': query['created']
            }
            orders.append(item)

        return HttpResponse(orders)

    def show(self, req, id):
        """
        Show the order detail according to order's id `id`.

        This method returns a dictionary with following keys:
            - number
            - items
            - price
            - freight
            - discount
            - address
            - status
            - created
        If no order found, 404 will returned.
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
        query = self.db.get_order(id)

        if not query:
            return webob.exc.HTTPNotFound()

        order = {
            'number': query['number'],
            'items': query['items'],
            'price': query['price'],
            'address': query['address'],
            'created': query['created'],
            }

        return HttpResponse(order)

    def create(self, req, body=None):
        """
        For creating item, body should not be None and
        should contains the following params:
            - address  the address of the order name:mobile:address
            - items    the items list [{'id': x, 'count': y}, ...]
            - price    the total price of the order  float
            - weight   the total weight of the order float
        """
        #try:
        #    token = req.headers['X-AUTH-TOKEN']
        #except KeyError:
        #    return webob.exc.HTTPUnauthorized()

        #try:
        #    payload = jwt.decode(token)
        #except jwt.InvalidTokenError:
        #    return webob.exc.HTTPUnauthorized()

        #uid = payload['uid']
        uid = 'nmg1769815'

        try:
            name = body.pop('name')
            mobile = body.pop('mobile')
            region = body.pop('region')
            address = body.pop('address')
            items = body.pop('items')
        except KeyError as exc:
            logger.error(exc)
            return webob.exc.HTTPBadRequest()

	logger.info("items", items)
        # __id__ = uuid.uuid4().hex
        number = utils.generate_order_number()
        status = 0
        uid = uid
        created = round(time.time() * 1000)
	
	total_price = 0
        for member in items:
	    __item__ = self.db.get_veg(member['id'])

            try:
                price = __item__['price']
            except KeyError as exc:
                logger.error(exc)
                return webob.exc.HTTPBadRequest()

	    total_price += price * member['count']

	freight = 0 if total_price > 49 else 10

	total_price = total_price + freight

        order = {
            # 'id': __id__,
            'number': number,
            'uid': uid,
            'name': name,
            'mobile': mobile,
            'region': region,
            'address': address,
            'status': status,
            'freight': freight,
            'price': total_price,
            'created': created
            }

        # FIXME(nmg): should catch exception if any
        self.db.add_order(order)

        """
        Inset item in table `order_item`.
        For doing this you should get the following value for each item:
            - id
            - number
            - iid
            - name
            - img
            - price
            - size
            - count
            - created
        """
        item_list = []
        for member in items:
            # FIXME(nmg): should catch exception if any
            __item__ = self.db.get_veg(member['id'])

            try:
                name = __item__['name']
                img = __item__['img']
                price = __item__['price']
                size = __item__['size']
            except KeyError as exc:
                logger.error(exc)
                return webob.exc.HTTPBadRequest()

            count = member['count'] 
            created = created
            __id__ = uuid.uuid4().hex
            item = {
                'id': __id__,
                'iid': id,
                'number': number,
                'name': name,
                'img': img,
                'price': price,
                'size': size,
                'count': count,
                'created': created
            }

            item_list.append(item)

        # FIXME(nmg): should catch exception if any
        self.db.add_order_items(item_list)

        return HttpResponse({'number': number, 'price': total_price}) 

    def delete(self, req, id):
        """
        delete item according to item id `id`
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
        self.db.delete_item(id)

        return Response(201)

    def update(self, req, id, status):
        """Updated order status"""
        try:
            token = req.headers['X-AUTH-TOKEN']
        except KeyError:
            return webob.exc.HTTPUnauthorized()

        try:
            jwt.decode(token)
        except jwt.InvalidTokenError:
            return webob.exc.HTTPUnauthorized()

        # FIXME(nmg): should catch exception if any
        self.db.update_order(id, status)

        return Response(201)


def create_resource():
    return wsgi.Resource(Controller())

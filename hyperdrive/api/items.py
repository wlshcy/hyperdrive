import webob.exc

from jsonschema import SchemaError, ValidationError
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse 
from hyperdrive.common import cfg
from hyperdrive.common import timeutils
from hyperdrive.base import Base

CONF=cfg.CONF

LOG=logging.getLogger(__name__)

class Controller(Base):
    def __init__(self):
	super(Controller,self).__init__()

    def index(self,request):
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

        querys = self.db.get_items()
        for query in querys:
            item = {
                'id': query.id,
                'name': query.name,
                'img': query.img,
                'price': query.price,
                'created': timeutils.isotime(query.created),
                }
            items.append(item)

        return HttpResponse(items)

    def show(self,request,id):
        """
        Show the item info according to item's id `id`.

        This method returns a dictionary with following keys:
            - id
            - name
            - img 
            - price 
            - size
            - origin 
        If no item found, empty dictionary will returned.
        """

	item = {}
        query= self.db.get_item(id)
        if query is not None:
            item = {
                'id': query.id,
                'name': query.name,
                'img': query.img,
                'price': query.price,
                'origin': query.origin,
                }

        return HttpResponse(item)

    
    def create(self,request,body=None):
        """
        For creating item, body should not be None and
        should contains the following params:
            - name        the name of the item 
            - img         the image's of the item 
            - price       the price of the item 
            - size        the size of the item
            - origin      the origin of the item  
        All the above parmas are not optional and have no default value.
        """
        """This schema is used for data validate."""
        schema = {
            "type": "object",
            "properties": {
                "name": {
                     "type": "string",
                     "minLength": 32,
                     "maxLength": 64,
                },
                "img": {
                     "type": "string",
                },
                "price": {
                    "type": "integer",
                },
                "size": {
                    "type": "integer",
                },
                "origin": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 255,
                },
            },       
            "required": ["name","img","price","size","origin"] 
        }
        
        try:
            self.validator(body,schema)
        except (SchemaError,ValidationError) as exc:
            LOG.error(exc) 
	    return webob.exc.HTTPBadRequest(explanation="Bad Paramaters")

        id = uuid.uuid4().hex
        name = body.pop('name')
        img = body.pop('img')
        price = body.pop('price')
        size = body.pop('size')
        origin = body.pop('origin')

        try:
	    self.db.add_item(dict(
                id=id,
                name=name,
                img=img,
                price=price,
                size=size,
                origin=origin))
        except Exception as exc:
	    LOG.error(exc)
            return Response(500)

	return Response(201) 

    def delete(self,request,id):
        """
        delete item according to item id `id`
        """
        try:
            self.db.delete_item(id)
        except Exception as exc:
            LOG.error(exc)
            return Response(500)
        
        return Response(201)

    def update(self, request, body):
        """Updated container information"""
        return NotImplementedError()

def create_resource():
    return wsgi.Resource(Controller())

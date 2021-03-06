import routes

from hyperdrive import wsgi
from hyperdrive.api.v1 import login 
from hyperdrive.api.v1 import vegetables
from hyperdrive.api.v1 import combos 
from hyperdrive.api.v1 import veg_slides
from hyperdrive.api.v1 import fruits
from hyperdrive.api.v1 import meats
from hyperdrive.api.v1 import specialties
from hyperdrive.api.v1 import orders
from hyperdrive.api.v1 import users
from hyperdrive.api.v1 import address
from hyperdrive.api.v1 import zone 
from hyperdrive.api.v1 import sms


class APIRouter(wsgi.Router):
    def __init__(self):
        self.mapper = routes.Mapper()
        self._setup_routes()

        super(APIRouter, self).__init__(self.mapper)

    def _setup_routes(self):
        """
        Setup RESTFUL routers.
        """

	self.mapper.connect('/vegetables/slides',
                            controller=vegetables.create_resource(),
                            action='slides',
                            conditions={'method': ['GET']})
        self.mapper.resource('vegetable', 'vegetables', controller=vegetables.create_resource())

        self.mapper.resource('combo', 'combos', controller=combos.create_resource())

	self.mapper.connect('/fruits/slides',
                            controller=vegetables.create_resource(),
                            action='slides',
                            conditions={'method': ['GET']})
        self.mapper.resource('fruit', 'fruits', controller=fruits.create_resource())

        self.mapper.resource('meat', 'meats', controller=meats.create_resource())

	self.mapper.connect('/specialties/slides',
                            controller=vegetables.create_resource(),
                            action='slides',
                            conditions={'method': ['GET']})
        self.mapper.resource('specialty', 'specialties', controller=specialties.create_resource())

        self.mapper.resource('order', 'orders', controller=orders.create_resource())

        self.mapper.resource('user', 'users', controller=users.create_resource())

        self.mapper.resource('address', 'addresses', controller=address.create_resource())

        self.mapper.resource('zone', 'zones', controller=zone.create_resource())

        self.mapper.connect('/login',
                            controller=login.create_resource(),
                            action='login',
                            conditions={'method': ['POST']})

        self.mapper.connect('/sms',
                            controller=sms.create_resource(),
                            action='create',
                            conditions={'method': ['POST']})

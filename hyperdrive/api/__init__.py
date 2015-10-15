import routes

from hyperdrive import wsgi
from hyperdrive.api import login 
from hyperdrive.api import items
from hyperdrive.api import orders
from hyperdrive.api import users
from hyperdrive.api import address
from hyperdrive.api import sms


class APIRouter(wsgi.Router):
    def __init__(self):
        self.mapper = routes.Mapper()
        self._setup_routes()

        super(APIRouter, self).__init__(self.mapper)

    def _setup_routes(self):
        """
        The following `mapper.resource` will generated the following routes:
        """

        self.mapper.resource('item', 'items', controller=items.create_resource())

        self.mapper.resource('order', 'orders', controller=orders.create_resource())

        self.mapper.resource('user', 'users', controller=users.create_resource())

        self.mapper.resource('address', 'addresses', controller=address.create_resource())

        self.mapper.connect('/login',
                            controller=login.create_resource(),
                            action='login',
                            conditions={'method': ['POST']})

        self.mapper.connect('/sms',
                            controller=sms.create_resource(),
                            action='create',
                            conditions={'method': ['POST']})

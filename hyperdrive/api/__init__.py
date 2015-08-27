import routes

from hyperdrive import wsgi
from hyperdrive.api import items


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

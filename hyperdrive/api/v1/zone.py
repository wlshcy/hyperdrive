import uuid
from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common.response import Response, HttpResponse
from hyperdrive.common import cfg
from hyperdrive.base import Base
import time
import webob.exc
from hyperdrive.common.exception import Fault
import jwt

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class Controller(Base):
    def __init__(self):
        super(Controller, self).__init__()

    def index(self, req):
        """
        List all zones
	"""
        
        zones = []
	
        zones =[{"name":"甘肃","code":"1028","children":
                   [{"name":"张掖市","children":[
                       {"name":"民乐县","children":
                           [
                               {"name": "城区","children":""},
                               {"name": "洪水镇","children":""},
                           ]
                       }]
                   }]
                }]

        return HttpResponse(zones)

def create_resource():
    return wsgi.Resource(Controller())

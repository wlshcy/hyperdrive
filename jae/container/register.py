from jae import db 
from jae.common import cfg
from jae.common import log as logging
import uuid
import netifaces
from sqlalchemy.exc import IntegrityError

CONF = cfg.CONF

LOG = logging.getLogger(__name__)

class Register(object):
    def __init__(self):
        self.db = db.API()

    def register(self,host,port):
	if host == '0.0.0.0':
	    host = CONF.my_id
	    if not host:
	        host = self.get_host()	
	"""
	use the last 12 bit of uuid1 to unique a machine.
	"""
	id = uuid.uuid1().hex[-12:]

	try:
            self.db.register(dict(
		             id=id,
		             host=host,
		             port=port))
	except IntegrityError:
	    """
	    already register? just pass.
	    """
	    pass

    def get_host(self):
	"""
	ifaces = netifaces.interfaces()
	nic = [ i for i in ifaces if i not in 'lo'][0]
	"""
	interface_name = CONF.interface_name
	if not interface_name:	
	    interface_name = 'eth0'
        addrs = netifaces.ifaddresses(interface_name)
	
	return addrs[netifaces.AF_INET][0]['addr']
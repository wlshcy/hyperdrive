__author__ = 'nmg'


__all__ = ['MongoAPI']

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from hyperdrive.common import log as logging
import sys
import time


logger = logging.getLogger(__name__)


class MongoAPI(object):
    def __init__(self, host, port, db):
        self.host = host
        self.port = int(port)
        self.db = db
        self.connection = None
        self.max_retries = 5
        self.retry_interval = 5

        self.connect()

    def connect(self):
        attempt = 0
        while True:
            attempt += 1
            try:
                self._connect()
                logger.info("Connecting to MongoDB server on {}:{} succeed".format(self.host, self.port))
                return
            except ConnectionFailure:
                logger.error("Connecting to MongoDB failed...retry after {} seconds".format(self.retry_interval))

            if attempt >= self.max_retries:
                logger.error("Connecting to MongoDB server on {}:{} falied".format(self.host, self.port))
                sys.exit(1)
            time.sleep(self.retry_interval)

    def _connect(self):
        self.connection = MongoClient(self.host, self.port)

    def add_item(self, item, coll='items'):
        """
        Insert items in collection.

        @param coll: the collection, default to `items`
        @param msg: the items be saved

        @return: a WriteResult object that contains the status of the operation(not used currently)
        """
        coll = self.connection[self.db][coll]

        return coll.insert(item)

    def get_items(self, invent='items'):
        """
        Get items from collection.

        @param invent: the collection

        @return: `pymongo.cursor.Cursor object`
        """

        coll = self.connection[self.db][invent]

        return coll.find({})

    def get_item(self,  __id__, invent='items'):
        """
        Get specified item according item id.

        @param invent: the item table
        @param id: the item id

        @return: `pymongo.cursor.Cursor object`
        """
        coll = self.connection[self.db][invent]

        return coll.find_one({'id': __id__})

    def delete_item(self, id, invent='items'):
        """
        Delete item according item id.
        @param id: the item id
        @param invent: the item table
        """
        coll = self.connection[self.db][invent]

        return coll.remove({'id': id})

    def update_item(self, __id__, data, invent='items'):
        """
        Update item information.
        @param data:
        @param invent:
        """
        query = {'id': __id__}
        update = {'$set': data}

        coll = self.connection[self.db][invent]

        return coll.update(query, update)

    def add_order(self, order, coll='orders'):
        """
        Insert items in collection.

        @param coll: the collection, default to `items`
        @param order: the order be saved

        @return: a WriteResult object that contains the status of the operation(not used currently)
        """
        coll = self.connection[self.db][coll]

        return coll.insert(order)

    def get_orders(self, user_id, invent='orders'):
        """
        Get orders from collection.

        @param invent: the collection

        @param user_id: the user id to retrieve

        @return: `pymongo.cursor.Cursor object`
        """

        coll = self.connection[self.db][invent]

        return coll.find({'uid': user_id})

    def get_order(self,  __id__, invent='orders'):
        """
        Get specified order according order id.

        @param invent: the item table
        @param id: the order id

        @return: `pymongo.cursor.Cursor object`
        """
        coll = self.connection[self.db][invent]

        return coll.find_one({'id': __id__})

    def delete_order(self, __id__, invent='orders'):
        """
        Delete item according order id.
        @param id: the order id
        @param invent: the order table
        """
        coll = self.connection[self.db][invent]

        return coll.remove({'id': __id__})

    def add_order_items(self, item_list, coll='order_items'):
        """
        Add order items in `order_items`
        @param item_list: order items list
        @param coll: table to insert
        """
        coll = self.connection[self.db][coll]

        return coll.insert(item_list)

    def add_user(self, user, coll='users'):
        """
        Add new user in user table `users`.

        @param user: the user object to be added
        @param coll: the user table to add to
        @return: nothing
        """
        coll = self.connection[self.db][coll]

        return coll.insert(user)

    def get_users(self, invent='users'):
        """
        Get all users.

        @param invent: the user table
        @return: `pymongo.cursor.Cursor object`
        """
        coll = self.connection[self.db][invent]

        return coll.find({})

    def get_user(self, mobile, invent='users'):
        """
        Get specified user by mobile
        @param mobile:
        @param invent:
        @return:
        """
        coll = self.connection[self.db][invent]

        return coll.find_one({'mobile': mobile})

    def add_address(self, address, invent='addresses'):
        """
        Add user address
        :param address: the address to be added
        :param invent: the address table
        :return:
        """
        coll = self.connection[self.db][invent]

        return coll.insert(address)

    def get_addresses(self, uid, invent='addresses'):
        """
        List all addresses filter by uid
        :param uid: the user id whose addresses will be list
        :param invent: address table
        :return: List of all addresses
        """
        coll = self.connection[self.db][invent]

        return coll.find({'uid': uid})

    def get_address(self, address_id, invent='addresses'):
        """
        Show specified address according address_id
        :param address_id: the address id
        :param invent: address table
        :return: Dict of address
        """
        coll = self.connection[self.db][invent]

        return coll.find_one({'id': address_id})

    def delete_address(self, address_id, invent='addresses'):
        """
        Delete address according to address_id
        :param address_id: the address to be deleted
        :param invent: address table
        :return: None
        """
        coll = self.connection[self.db][invent]

        return coll.remove({'id': address_id})

    def update_address(self, __id__, data, invent='addresses'):
        """
        Update address information
        :param id: the address to be updated
        :param body: the content to be updated
        :param invent: address table
        :return: None
        """
        query = {'id': __id__}
        update = {'$set': data}

        coll = self.connection[self.db][invent]

        return coll.update(query, update)

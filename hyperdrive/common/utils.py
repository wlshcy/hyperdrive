import random
import os
import time

_SALT_BYTE_SIZE = 24
_HASH_BYTE_SIZE = 24

def generate_order_number():
    """Generate order number"""
    prefix = time.strftime("%Y%m%d", time.localtime())
    suffix = str(random.randint(0, 99999999)).zfill(8)

    return "".join([prefix, suffix])


def encrypt_password(password):
    salt = os.urandom(_SALT_BYTE_SIZE)


if __name__ == '__main__':
    print(generate_order_number())
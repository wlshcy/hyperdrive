import random
import uuid
import hashlib
import time
import datetime
import jwt

_TOKEN_SECRET = 'ef1dfe5b4cb94ec4b38f57e4aa304116'

_TOKEN_EXPIRED_SECONDS = 86400


def generate_order_number():
    """Generate order number"""
    prefix = time.strftime("%Y%m%d", time.localtime())
    suffix = str(random.randint(0, 99999999)).zfill(8)

    return "".join([prefix, suffix])


def encrypt_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def generate_token(user_id):
    payload = {'id': user_id,
               'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=_TOKEN_EXPIRED_SECONDS)}

    return jwt.encode(payload, _TOKEN_SECRET)

if __name__ == '__main__':
    print(generate_order_number())
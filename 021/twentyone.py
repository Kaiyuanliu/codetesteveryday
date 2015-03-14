# -*- coding: utf-8 -*-

import bcrypt
import hashlib


class HashPassword(object):

    def __init__(self, method="bcrypt"):
        self._method = method

    @property
    def crypt_method(self):
        return self._method

    @crypt_method.setter
    def crypt_method(self, method):
        self._method = method

    def hash_password(self, input_password):
        result = getattr(self, '_hash_password_with_'+self._method, None)
        if result:
            return result(input_password)

    def _hash_password_with_bcrypt(self, input_password):
        return bcrypt.hashpw(input_password, bcrypt.gensalt())

    def _hash_password_with_sha256(self, input_password):
        import uuid
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + input_password.encode()).hexdigest() + ":" + salt

    def check_password(self, hashed_password, input_password):
        result = getattr(self, '_check_password_with_'+self._method, None)
        if result:
            return result(hashed_password, input_password)
        else:
            raise ValueError("wrong input parameters while checking password")

    def _check_password_with_bcrypt(self, hashed_password, input_password):
        return bcrypt.hashpw(input_password, hashed_password) == hashed_password

    def _check_password_with_sha256(self, hashed_password, input_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + input_password.encode()).hexdigest()


if __name__ == "__main__":
    hash_password = HashPassword("sha256")
    input_password = "tested"
    hashed_password = hash_password.hash_password(input_password)
    if hash_password.check_password(hashed_password, input_password):
        print "correct"
    else:
        print "wrong"

import libnacl
import base64
import logging
from json import dumps


log = logging.getLogger()


class SignatureError(Exception):
    def __init__(self, message, errors):
        super(self).__init__(message)
        self.errors = errors


def validateSignature(signature, key, message):
    try:
        original = libnacl.crypto_sign_open(base64.b64decode(signature), base64.b64decode(key))
        if bytes(message, 'utf-8') == original:
            return 'success'
        return 'message and signature does not match'
    except ValueError as err:
        raise SignatureError(dumps({"error": err, "status": 400, "message": "invalid signature"}))

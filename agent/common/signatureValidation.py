import libnacl
import base64
import logging
from json import loads
from agent.common.errorMessages import SIGNATURE_MESSAGE_MISMATCH, INVALID_SIGNATURE


log = logging.getLogger()


class SignatureError(Exception):
    pass


def validateSignature(signature, key, data):
    try:
        verificationData = loads(data)
        original = libnacl.crypto_sign_open(base64.b64decode(signature), base64.b64decode(key))
        if bytes(verificationData['message'], 'utf-8') == original:
            return True, 'Success'
        return False, SIGNATURE_MESSAGE_MISMATCH
    except ValueError:
        raise SignatureError(INVALID_SIGNATURE)

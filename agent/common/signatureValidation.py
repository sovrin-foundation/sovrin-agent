import libnacl
import base64
import logging
from agent.common.errorMessages import SIGNATURE_VALIDATION, SIGNATURE_MESSAGE_INVALID


log = logging.getLogger()


class SignatureError(Exception):
    pass


def validateSignature(signature, key, message):
    try:
        original = libnacl.crypto_sign_open(base64.b64decode(signature), base64.b64decode(key))
        if bytes(message, 'utf-8') == original:
            return 'success'
        return SIGNATURE_MESSAGE_INVALID
    except ValueError:
        raise SignatureError(SIGNATURE_VALIDATION)

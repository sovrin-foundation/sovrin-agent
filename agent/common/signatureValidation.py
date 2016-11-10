import libnacl
import base64
import logging


log = logging.getLogger()


def validateSignature(signature, key, message):
    try:
        original = libnacl.crypto_sign_open(base64.b64decode(signature), base64.b64decode(key))
        return bytes(message, 'utf-8') == original
    except Exception as e:
        log.info(e)

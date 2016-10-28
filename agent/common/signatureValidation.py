import libnacl
import base64


def validate_signature(signature, key, message):
    try:
        original = libnacl.crypto_sign_open(base64.b64decode(signature), base64.b64decode(key))
        return bytes(message, 'utf-8') == original
    except Exception as e:
        print(str(e))

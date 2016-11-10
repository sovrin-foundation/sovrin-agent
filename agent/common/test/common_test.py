import libnacl
import base64

from agent.common.signatureValidation import validate_signature


def test_signature_validation():
    vk, sk = libnacl.crypto_sign_keypair()
    msg = 'this is a test'
    signed = libnacl.crypto_sign(bytes(msg, 'utf-8'), sk)
    base64Signature = base64.b64encode(signed)
    base64Key = base64.b64encode(vk)
    assert validate_signature(base64Signature, base64Key, msg)

import libnacl
import base64
from json import dumps

from agent.common.signatureValidation import validateSignature


def testSignatureValidation():
    vk, sk = libnacl.crypto_sign_keypair()
    data = {'message': 'this is a test'}
    signed = libnacl.crypto_sign(bytes(data['message'], 'utf-8'), sk)
    base64Signature = base64.b64encode(signed)
    base64Key = base64.b64encode(vk)
    verified, message = validateSignature(base64Signature, base64Key, dumps(data))
    assert verified
    data = {'message': 'this will fail'}
    verified, message = validateSignature(base64Signature, base64Key, dumps(data))
    assert not verified
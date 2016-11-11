from json import dumps


ALREADY_REGISTERED = dumps({
    "error": {
        "code": 409,
        "message": "User already registered"
    }
})

SIGNATURE_VALIDATION = dumps({
    "error": {
        "status": 400,
        "message": "invalid signature"
    }
})

SIGNATURE_MESSAGE_INVALID = dumps({
    "error": {
        "status": 400,
        "message": "decrypted message and sent message does not match"
    }
})

FORBIDDEN = dumps({"status": 401, "message": "not authorised"})
INVALID_DATA = dumps({"status": 400, "message": "invalid request"})
NOT_FOUND = dumps({"status": 404, "message": "not found"})
INVALID_INVITATION = dumps({"status": 400, "message": "invalid invitation"})
INVALID_CLAIM = dumps({"status": 400, "message": "invalid claim"})

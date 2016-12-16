ALREADY_REGISTERED = {
    "error": {
        "code": 409,
        "message": "User already registered"
    }
}

INVALID_SIGNATURE = {
    "error": {
        "status": 400,
        "message": "invalid signature"
    }
}

SIGNATURE_MESSAGE_MISMATCH = {
    "error": {
        "status": 400,
        "message": "decrypted message and sent message does not match"
    }
}

FORBIDDEN = {
    'error': {
        "status": 401,
        "message": "not authorised"
    }
}

INVALID_DATA = {
    'error': {
        "status": 400,
        "message": "invalid request"
    }
}

NOT_FOUND = {
    'error': {
        "status": 404,
        "message": "not found"
    }
}

INVALID_INVITATION = {
    'error': {
        "status": 400,
        "message": "invalid invitation"
    }
}

INVALID_CLAIM = {
    'error': {
         "status": 400,
         "message": "invalid claim"
    }
}

USER_NOT_FOUND = {
    'error': {
        'status': 400,
        'message': 'user not found'
    }
}
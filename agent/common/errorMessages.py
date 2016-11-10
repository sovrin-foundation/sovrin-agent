from json import dumps


FORBIDDEN = dumps({"status": 401, "message": "not authorised"})
INVALID_DATA = dumps({"status": 403, "message": "invalid request"})
NOT_FOUND = dumps({"status": 404, "message": "not found"})
INVALID_INVITATION = dumps({"status": 403, "message": "invalid invitation"})
INVALID_CLAIM = dumps({"status": 403, "message": "invalid claim"})


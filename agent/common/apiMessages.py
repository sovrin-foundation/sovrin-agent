from json import dumps


SOCKET_CONNECTED = dumps({'type': 'open', 'message': 'Socket connected'})
SOCKET_CLOSED = dumps({'type': 'closed', 'message': 'Socket closed'})

REGISTER_SUCCESS = {
    'success': {
        "type": "register",
        "success": True,
        "status": 200
    }
}

LOGIN_SUCCESS = {
    'success': {
        "type": "login",
        "success": True,
        "status": 200
    }
}
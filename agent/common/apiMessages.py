from json import dumps


SOCKET_CONNECTED = dumps({'type': 'open', 'message': 'Socket connected'})
SOCKET_CLOSED = dumps({'type': 'closed', 'message': 'Socket closed'})

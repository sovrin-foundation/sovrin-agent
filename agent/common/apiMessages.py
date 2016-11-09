from json import dumps


apiMessages = {
    "SOCKET_CONNECTED": dumps({'type': 'open', 'message': 'Socket connected'}),
    "SOCKET_CLOSED": dumps({'type': 'closed', 'message': 'Socket closed'})
}

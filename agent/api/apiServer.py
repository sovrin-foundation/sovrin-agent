import aiohttp_cors
import sockjs
import json

from aiohttp.web import Application
from jsonschema import ValidationError

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.onboarding.api.onboard import onboard
from agent.login.api.login import login
from agent.links.api.invitation import acceptInvitation
from agent.claims.api.claims import getClaim
from agent.common.apiMessages import SOCKET_CONNECTED, SOCKET_CLOSED
from agent.common.errorMessages import INVALID_DATA

async def handleWebsocketData(data):
    routeMap = {
        'acceptInvitation': acceptInvitation,
        'getClaim': getClaim,
        'login': login,
        'register': onboard
    }
    try:
        return await routeMap[data['route']](data)
    except (TypeError, KeyError, ValidationError):
        return INVALID_DATA

async def websocketHandler(msg, session):
    if msg.tp == sockjs.MSG_OPEN:
        session.manager.broadcast(SOCKET_CONNECTED)
    elif msg.tp == sockjs.MSG_MESSAGE:
        requestData = json.loads(msg.data)
        responseData = await handleWebsocketData(requestData)
        session.manager.broadcast(responseData)
    elif msg.tp == sockjs.MSG_CLOSED:
        session.manager.broadcast(SOCKET_CLOSED)


def api(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])
    sockjs.add_endpoint(app, prefix='/v1/wsConnection', handler=websocketHandler)

    # Enable CORS on all APIs
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        if route.name is not None and not route.name.startswith('sock'):
            cors.add(route)

    return app

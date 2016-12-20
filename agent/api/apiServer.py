
import aiohttp_cors
import asyncio
import sockjs
import json

from aiohttp.web import Application, json_response
import aiohttp
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


async def httphandler(request, data):
    if request.path == "/acceptInvitation":
        async with aiohttp.ClientSession(loop=request.app.loop) as session:
            result = await acceptInvitation(data, session, 'http://localhost:8100/getClaims')
            print(result)
            return json_response(result)
    elif request.path == "/getClaims":
        result = await getClaim(data)
        return json_response(result)

async def fetch(session, url):
    async with session.post(url) as response:
        return await response.text()


def api(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])
    sockjs.add_endpoint(app, prefix='/v1/wsConnection', handler=websocketHandler)
    app.router.add_post('/acceptInvitation', httphandler)
    app.router.add_post('/getClaims', httphandler)

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

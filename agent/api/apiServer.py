import aiohttp_cors
import sockjs
import json

from aiohttp.web import Application

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.onboarding.api.onboard import onboard
from agent.login.api.login import login
from agent.links.api.invitation import acceptInvitation
from agent.claims.api.claims import getClaim

async def handleWebsocketData(data):
    switcher = {
        'acceptInvitation': acceptInvitation,
        'getClaim': getClaim
    }
    return await switcher[data['type']](data)


async def websocketHandler(msg, session):
    if msg.tp == sockjs.MSG_OPEN:
        session.manager.broadcast(json.dumps({'type': 'open', 'message': 'Socket connected'}))
    elif msg.tp == sockjs.MSG_MESSAGE:
        requestData = json.loads(msg.data)
        responseData = await handleWebsocketData(requestData)
        session.manager.broadcast(responseData)
    elif msg.tp == sockjs.MSG_CLOSED:
        session.manager.broadcast(json.dumps({'type': 'closed', 'message': 'Socket closed'}))


def api(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])
    sockjs.add_endpoint(app, prefix='/v1/sockjs', handler=websocketHandler)
    app.router.add_post('/v1/login', login)
    app.router.add_post('/v1/onboard', onboard)

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

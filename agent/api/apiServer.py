import aiohttp_cors
import sockjs
import json

from aiohttp import web, WSMsgType
from jsonschema import validate

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.onboarding.api.onboard import onboard
from agent.login.api.login import login
from agent.links.api.invitation import acceptInvitation
from agent.claims.api.claims import getClaim


async def login(request, data):
    validate(data, loginSchema)
    return web.json_response(data={"success": True})


async def register(request, data):
    validate(data, registerSchema)
    return web.json_response(data={"success": True})


async def acceptInvitation(data):
    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        response = invitations[invitationId]
        response['type'] = data['type']
        return json.dumps({"type": data['type'],
                           "claims": invitations[invitationId]['claims'],
                           "linkId": data["invitation"]["id"]})

    return json.dumps(data={"type": "error", "error": "No invitation found"})

async def getClaim(data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return json.dumps({"claims": claims, "type": 'getClaim'})

    return json.dumps(data={"type": "error", "error": "No invitation found"})


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
    app.router.add_post('/v1/register', register)

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

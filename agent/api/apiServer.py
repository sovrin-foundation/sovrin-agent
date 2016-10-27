import aiohttp_cors

from aiohttp import web
from jsonschema import validate

from agent.schema.requestSchema import registerSchema, loginSchema, \
    acceptInvitationSchema, getClaimSchema
from agent.api.data.sample import invitations
from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware


async def login(request, data):
    validate(data, loginSchema)
    return web.json_response(data={"success": True})


async def register(request, data):
    validate(data, registerSchema)
    return web.json_response(data={"success": True})


async def acceptInvitation(request, data):
    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        return web.json_response(data=invitations[invitationId])

    return web.json_response(data={"error": "No invitation found"})

async def getClaim(request, data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return web.json_response(data={"claims": claims})

    return web.json_response(data={"error": "No invitation found"})


def startApi():
    app = web.Application(middlewares=[jsonParseMiddleware])

    app.router.add_post('/v1/login', login)
    app.router.add_post('/v1/register', register)
    app.router.add_post('/v1/acceptInvitation', acceptInvitation)
    app.router.add_post('/v1/getClaim', getClaim)

    # Enable CORS on all APIs
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app)

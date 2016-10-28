import aiohttp_cors

from aiohttp.web import Application

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.onboarding.api.onboard import onboard
from agent.login.api.login import login
from agent.links.api.invitation import acceptInvitation
from agent.claims.api.claims import getClaim


def api(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])

    app.router.add_post('/v1/login', login)
    app.router.add_post('/v1/onboard', onboard)
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

    return app

import logging
import aiohttp_cors
import sockjs

from jsonschema import ValidationError
from aiohttp.web import Application

from plenum.common.looper import Looper
from plenum.common.signer_simple import SimpleSigner
from sovrin.client.wallet.wallet import Wallet
from sovrin.agent.agent import createAgent, WalletedAgent
from sovrin.client.client import Client

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.common.signatureValidation import SignatureError
from agent.onboarding.api.onboard import onboard, onboardHttp
from agent.login.api.login import login, loginHttp
from agent.links.api.invitation import acceptInvitation, acceptInvitationHttp
from agent.claims.api.claims import getClaim, getClaimHttp
from agent.common.apiMessages import SOCKET_CONNECTED, SOCKET_CLOSED
from agent.common.errorMessages import INVALID_DATA
from json import dumps

log = logging.getLogger()


async def handleWebSocketRequest(data, app):
    # TODO:SC Add version in route as well
    routeMap = {
        'acceptInvitation': acceptInvitation,
        'getClaim': getClaim,
        'login': login,
        'register': onboard
    }
    try:
        return await routeMap[data['route']](data, app)
    except SignatureError as err:
        return err
    except (TypeError, KeyError, ValidationError):
        return dumps(INVALID_DATA)


async def webSocketConnectionHandler(msg, session):
    if msg.tp == sockjs.MSG_OPEN:
        session.manager.broadcast(SOCKET_CONNECTED)
    elif msg.tp == sockjs.MSG_MESSAGE:
        # TODO:SC handle json parse error, schema error
        requestData = json.loads(msg.data)
        responseData = await handleWebSocketRequest(requestData, session.registry)
        session.manager.broadcast(responseData)
    elif msg.tp == sockjs.MSG_CLOSED:
        session.manager.broadcast(SOCKET_CLOSED)


def startAgent(name, seed, loop=None):
    agentWallet = Wallet(name)
    agentWallet.addIdentifier(signer=SimpleSigner(seed=bytes(seed, 'utf-8')))
    agent = createAgent(WalletedAgent, name, wallet=agentWallet, loop=loop)
    agentPort = agent.endpoint.stackParams['ha'].port
    with Looper(debug=True) as looper:
        looper.add(agent)
        log.debug("Running {} now (port: {})".format(name, agentPort))

    return agent


def newApi(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])
    sockjs.add_endpoint(app, prefix='/v1/wsConnection', handler=webSocketConnectionHandler)
    app.router.add_post('/v1/login', loginHttp)
    app.router.add_post('/v1/onboard', onboardHttp)
    app.router.add_post('/v1/acceptInvitation', acceptInvitationHttp)
    app.router.add_post('/v1/getClaim', getClaimHttp)

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

    # In memory list of registered users, not using any database intentionally
    app['users'] = {}

    return app

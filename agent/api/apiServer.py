import logging
from json import dumps

import aiohttp_cors
import sockjs
from aiohttp.web import Application
from aiohttp.web_reqrep import json_response
from jsonschema import ValidationError

from agent.api.logic import handleMsg
from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.common.apiMessages import SOCKET_CONNECTED, SOCKET_CLOSED
from agent.common.errorMessages import INVALID_DATA
from agent.common.signatureValidation import SignatureError
from plenum.common.looper import Looper
from plenum.common.signer_simple import SimpleSigner
from sovrin_client.agent.agent import createAgent, WalletedAgent
from sovrin_client.client.wallet.wallet import Wallet

log = logging.getLogger()


async def handleWebSocketRequest(data, app):
    # TODO:SC Add version in route as well
    try:
        res = await handleMsg(data['route'], data, app)
        return dumps(res)
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


async def v1(request, data):
    res = await handleMsg(request.match_info['resource'], data, request.app)
    return json_response(data=res)


def newApi(loop):
    app = Application(loop=loop, middlewares=[jsonParseMiddleware])
    sockjs.add_endpoint(app, prefix='/v1/wsConnection', handler=webSocketConnectionHandler)
    app.router.add_post('/v1/{resource}', v1)

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

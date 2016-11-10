import logging

import aiohttp_cors

from aiohttp.web import Application
from plenum.common.looper import Looper

from agent.api.middlewares.jsonParseMiddleware import jsonParseMiddleware
from agent.onboarding.api.onboard import onboard
from agent.login.api.login import login
from agent.links.api.invitation import acceptInvitation
from agent.claims.api.claims import getClaim

from plenum.common.signer_simple import SimpleSigner
from sovrin.client.wallet.wallet import Wallet
from sovrin.agent.agent import runAgent, WalletedAgent
from sovrin.client.client import Client


log = logging.getLogger()


def startAgent(name, seed):

    class ApiAgent(WalletedAgent):
        def __init__(self,
                     basedirpath: str,
                     client: Client = None,
                     wallet: Wallet = None,
                     port: int = None):
            super().__init__(name, basedirpath, client, wallet, port)

    agentWallet = Wallet(name)
    agentWallet.addIdentifier(signer=SimpleSigner(seed=bytes(seed, 'utf-8')))
    agent = runAgent(ApiAgent, name, wallet=agentWallet, startRunning=False)
    agentPort = agent.endpoint.stackParams['ha'].port
    with Looper(debug=True) as looper:
        looper.add(agent)
        log.debug("Running {} now (port: {})".format(name, agentPort))
        looper.run()

    return agent


def api(loop, name, seed):
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

    agent = startAgent(name, seed)
    # Add agent to app instance to allow it to be accessible
    # from all api requests
    app['agent'] = agent

    return app

from typing import Dict

import pytest

from agent.api.apiServer import newApi
from agent.api.logic import Logic
from agent.extension.extension import ApiInterface, Extension, \
    ApiExtension
from agent.extension.interface import Interface, ApiInterface
from plenum.common.eventually import eventually
from plenum.common.motor import Motor
from plenum.test.helper import assertFunc


# trying some things out here; if they work out, we can move them out of test

class HasApi:
    """
    Mixin for Agent.
    Adds an API and associated behaviors.
    """
    def __init__(self, loop):
        self.api = newApi(loop=loop)


class NewAgent(Motor, Logic):
    def __init__(self, name: str):
        Motor.__init__(self)
        Logic.__init__(self)
        self._last_loop = None
        self._name = name
        self._interfaces = {}  # type: Dict[str, Interface]

    def name(self):
        return self._name

    def loadExtension(self, extension: Extension):
        for i in extension.get_interfaces():
            self._interfaces[i.name()] = i
            i.start(self._last_loop)
        d = {i.name(): i for i in extension.get_interfaces()}
        self._interfaces.update(d)

    async def prod(self, limit) -> int:
        s = 0
        for i in self._interfaces.values():
            s += await i.prod(limit)
        return s

    def _statusChanged(self, old, new):
        pass

    def start(self, loop):
        self._last_loop = loop
        for iface in self._interfaces.values():
            iface.start(loop)
        super().start(loop)

    def onStopping(self, *args, **kwargs):
        for iface in self._interfaces.values():
            iface.stop(*args, **kwargs)


@pytest.fixture()
def looper(txnPoolNodesLooper):
    return txnPoolNodesLooper


@pytest.fixture()
def api_extension(looper):
    return ApiExtension('api1')


@pytest.fixture()
def api_client(looper, test_client, api_extension):
    return looper.run(test_client(api_extension.get_interfaces()[0]._api))


@pytest.fixture()
def agent(looper, api_extension):
    a = NewAgent('agent1')
    a.loadExtension(api_extension)
    looper.add(a)
    looper.startall()
    return a


def testNewAgent(looper, agent, api_extension, api_client):
    response = looper.run(api_client.get('/'))
    assert response.status == 404
    # test_api_client
    # looper.runFor(2)


def testNewAgentWithApi(nodeSet, looper, walletBuilder, agentBuilder): #, api, aliceAgent, aliceAgentConnected):
    wallet = walletBuilder('Bob')
    agent = agentBuilder(wallet)
    looper.add(agent)
    looper.run(eventually(assertFunc, agent.client.isReady))

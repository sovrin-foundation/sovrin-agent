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
        self._name = name
        self._interfaces = {}  # type: Dict[str, Interface]

    def name(self):
        return self._name

    def loadExtension(self, extension: Extension):
        d = {i.name(): i for i in extension.getInterfaces()}
        self._interfaces.update(d)

    async def prod(self, limit) -> int:
        s = 0
        for i in self._interfaces.values():
            s += await i.prod(limit)
        return s

    def _statusChanged(self, old, new):
        pass

    def start(self, loop):
        for iface in self._interfaces.values():
            iface.start(loop)
        super().start(loop)

    def onStopping(self, *args, **kwargs):
        for iface in self._interfaces.values():
            iface.stop(*args, **kwargs)


@pytest.fixture()
def looper(txnPoolNodesLooper):
    return txnPoolNodesLooper


def testNewAgent(looper):
    agent = NewAgent('agent1')
    agent.loadExtension(ApiExtension('api1'))
    looper.add(agent)
    looper.runFor(2)


def testNewAgentWithApi(nodeSet, looper, walletBuilder, agentBuilder): #, api, aliceAgent, aliceAgentConnected):
    wallet = walletBuilder('Bob')
    agent = agentBuilder(wallet)
    looper.add(agent)
    looper.run(eventually(assertFunc, agent.client.isReady))

from abc import abstractmethod
from typing import Callable, Any, Dict

import pytest
from aiohttp.web import Application

from agent.api.apiServer import newApi
from agent.api.logic import Logic
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


class Interface(Motor):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def name(self):
        return self._name

    @abstractmethod
    def sendMsg(self, msg, to):
        raise NotImplementedError

    @abstractmethod
    def setReceiver(self, receiver):
        # receiver is a callable with this signature receive(msg, from) -> response
        raise NotImplementedError


class NewAgent(Motor):
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.interfaces = {}  # type: Dict[str, Interface]

    def name(self):
        return self._name

    async def prod(self, limit) -> int:
        s = 0
        for i in self.interfaces.values():
            s += await i.prod(limit)
        return s

    def _statusChanged(self, old, new):
        pass

    def start(self, loop):
        for iface in self.interfaces.values():
            iface.start(loop)
        super().start(loop)

    def onStopping(self, *args, **kwargs):
        for iface in self.interfaces.values():
            iface.stop( *args, **kwargs)


class NewApi(Interface):
    def __init__(self, name):
        super().__init__(name)
        self._api = None  # type: Application
        self._logic = Logic()

    def start(self, loop):
        self._api = newApi(loop, self._logic)
        super().start(loop)

    def setReceiver(self, receiver):
        # TODO
        raise NotImplementedError

    def sendMsg(self, msg, to):
        # TODO
        raise NotImplementedError

    async def prod(self, limit) -> int:
        return 0

    def _statusChanged(self, old, new):
        pass

    def onStopping(self, *args, **kwargs):
        if self._api is None:
            self._api.loop.run_until_complete(self.shutdown())
            self._api = None


@pytest.fixture()
def looper(txnPoolNodesLooper):
    return txnPoolNodesLooper


def testNewAgent(looper):
    agent = NewAgent('agent1')
    agent.interfaces['api'] = NewApi('api1')
    looper.add(agent)
    looper.runFor(2)

#
# def testNewAgentWithApi(nodeSet, looper, walletBuilder, agentBuilder): #, api, aliceAgent, aliceAgentConnected):
#     wallet = walletBuilder('Bob')
#     agent = agentBuilder(wallet)
#     looper.add(agent)
#     looper.run(eventually(assertFunc, agent.client.isReady))

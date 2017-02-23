from abc import abstractmethod

from aiohttp.web import Application

from agent.api.apiServer import newApi
from agent.api.logic import HandlesMessages, Logic
from plenum.common.motor import Motor


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


class ApiInterface(Interface):
    def __init__(self, name, msgHandler: HandlesMessages=None):
        super().__init__(name)
        self._api = None  # type: Application
        self.msgHandler = msgHandler or Logic()

    def start(self, loop):
        self._api = newApi(loop, self.msgHandler)
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

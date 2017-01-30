from abc import abstractmethod
from typing import List

from agent.api.logic import Logic
from agent.extension.interface import Interface, ApiInterface


class Extension:
    @abstractmethod
    def getInterfaces(self) -> List[Interface]:
        raise NotImplementedError


class ApiExtension(Extension):
    def __init__(self, name: str):
        self._logic = Logic()
        self._api = ApiInterface(name, self._logic)

    def getInterfaces(self):
        return [self._api]



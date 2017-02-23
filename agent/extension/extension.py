from abc import abstractmethod
from typing import List

from agent.api.logic import Logic
from agent.extension.interface import Interface, ApiInterface


class Extension:
    @abstractmethod
    def get_interfaces(self) -> List[Interface]:
        raise NotImplementedError


class ApiExtension(Extension):
    def __init__(self, name: str):
        self._logic = Logic()
        self._api_iface = ApiInterface(name, self._logic)

    def get_interfaces(self):
        return [self._api_iface]



from abc import ABC, abstractmethod


class GatewayABC(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def send(self) -> str:
        pass

    @abstractmethod
    def delete(self):
        pass

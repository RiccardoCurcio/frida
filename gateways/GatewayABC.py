from abc import ABC, abstractmethod


class GatewayABC(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def delete(self):
        pass

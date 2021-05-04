from abc import ABC, abstractmethod


class GatewayABC(ABC):

    def __init__(self, logger):
        self.__logger = logger
        pass

    @abstractmethod
    def send(self) -> str:
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def check(self) -> bool:
        pass

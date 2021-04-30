import typing
from configparser import ConfigParser
from src.application.command import Command


class ClearCommand(Command):

    def __init__(
        self,
        config: ConfigParser,
        services: list,
        overrideGateway: typing.Union[list, None] = None,
        overrideClearGatewayExcept: typing.Union[str, None] = None,
        overrideClearInterval: typing.Union[int, None] = None
    ):
        self._config = config
        self._services = services
        self._overrideGateway = overrideGateway
        self._overrideClearGatewayExcept = overrideClearGatewayExcept
        self._overrideClearInterval = overrideClearInterval
        pass

    @property
    def config(self) -> ConfigParser:
        return self._config

    @config.setter
    def config(self, config: ConfigParser):
        self._config = config

    @property
    def services(self) -> list:
        return self._services

    @services.setter
    def services(self, services: list):
        self._services = services

    @property
    def overrideGateway(self) -> typing.Union[list, None]:
        return self._overrideGateway

    @overrideGateway.setter
    def overrideGateway(
        self,
        overrideGateway: typing.Union[list, None] = None
    ):
        self._overrideGateway = overrideGateway

    @property
    def overrideClearGatewayExcept(self) -> typing.Union[str, None]:
        return self._overrideClearGatewayExcept

    @overrideClearGatewayExcept.setter
    def overrideClearGatewayExcept(
        self,
        overrideClearGatewayExcept: typing.Union[str, None] = None
    ):
        self._overrideClearGatewayExcept = overrideClearGatewayExcept

    @property
    def overrideClearInterval(self) -> typing.Union[int, None]:
        return self._overrideClearInterval

    @overrideClearInterval.setter
    def overrideClearInterval(
        self,
        overrideClearInterval: typing.Union[int, None] = None
    ):
        self._overrideClearInterval = overrideClearInterval

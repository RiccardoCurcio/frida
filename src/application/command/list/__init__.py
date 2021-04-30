from configparser import ConfigParser
from src.application.command import Command


class ListCommand(Command):

    def __init__(
        self,
        config: ConfigParser,
        services: list
    ):
        self._config = config
        self._services = services
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

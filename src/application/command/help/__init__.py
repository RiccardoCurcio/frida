from configparser import ConfigParser
from src.application.command import Command


class HelpCommand(Command):

    def __init__(
        self,
        config: ConfigParser
    ):
        self._config = config
        pass

    @property
    def config(self) -> ConfigParser:
        return self._config

    @config.setter
    def config(self, config: ConfigParser):
        self._config = config

import logging
from configparser import ConfigParser
from src.application.handler.handler import Handler
from src.application.command.version import VersionCommand
from src.process.version import VersionProcess


class Version(Handler):

    def __init__(
        self,
        config: ConfigParser,
        logger: logging.Logger,
        args: list
    ):
        self.logger = logger
        self.__config = config
        pass

    def run(self):
        VersionProcess(
            self.logger,
            VersionCommand(self.__config)
        ).run()
        pass

import logging
from configparser import ConfigParser
from src.cliOption.service import Service
from src.application.handler.handler import Handler
from src.application.command.check import CheckCommand
from src.process.check import CheckProcess


class Check(Handler):

    def __init__(
        self,
        config: ConfigParser,
        logger: logging.Logger,
        args: list
    ):
        self.logger = logger
        self.__config = config
        self.__services = Service.getOnlyService(args, logger, config)
        pass

    def run(self) -> None:
        """[run]
        """
        CheckProcess(
            self.logger,
            CheckCommand(self.__config, self.__services)
        ).run()
        pass

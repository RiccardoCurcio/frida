import logging
from configparser import ConfigParser
from src.cliOption.service import Service
from src.application.handler.handler import Handler
from src.application.command.list import ListCommand
from src.process.list import ListProcess


class List(Handler):

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

    def run(self):
        ListProcess(
            self.logger,
            ListCommand(self.__config, self.__services)
        ).run()
        pass

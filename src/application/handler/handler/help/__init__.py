import logging
from configparser import ConfigParser
from src.application.handler.handler import Handler
from src.application.command.help import HelpCommand
from src.process.help import HelpProcess


class Help(Handler):

    def __init__(
        self,
        config: ConfigParser,
        logger: logging.Logger,
        args: list
    ):
        self.logger = logger
        self.__config = config
        pass

    def run(self) -> None:
        """[run]
        """
        HelpProcess(
            self.logger,
            HelpCommand(self.__config)
        ).run()
        pass

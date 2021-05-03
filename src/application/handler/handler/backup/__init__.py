import logging
from configparser import ConfigParser
from src.cliOption.service import Service
from src.cliOption.overrideGateway import OverrideGateway
from src.application.handler.handler import Handler
from src.application.command.backup import BackupCommand
from src.process.backup import BackupProcess


class Backup(Handler):

    def __init__(
        self,
        config: ConfigParser,
        logger: logging.Logger,
        args: list
    ):
        self.logger = logger
        self.__config = config
        self.__services = Service.getOnlyService(args, logger, config)
        self.__overrideGateway = OverrideGateway.setGateway(args, logger)
        pass

    def run(self) -> None:
        """[Run]
        """
        BackupProcess(
            self.logger,
            BackupCommand(
                self.__config,
                self.__services,
                self.__overrideGateway
            )
        ).run()
        pass

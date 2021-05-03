import logging
from configparser import ConfigParser
from src.cliOption.service import Service
from src.cliOption.overrideGateway import OverrideGateway
from src.cliOption.overrideClearGatewayExcept import OverrideClearGatewayExcept
from src.cliOption.clearInterval import ClearInterval
from src.application.handler.handler import Handler
from src.application.command.clear import ClearCommand
from src.process.clear import ClearProcess


class Clear(Handler):

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
        self.__overrideClearGatewayExcept = OverrideClearGatewayExcept.setClearGatewayExcept(args, logger)
        self.__overrideClearInterval = ClearInterval.setClearInterval(args, logger)
        pass

    def run(self) -> None:
        """[run]
        """
        ClearProcess(
            self.logger,
            ClearCommand(
                self.__config,
                self.__services,
                self.__overrideGateway,
                self.__overrideClearGatewayExcept,
                self.__overrideClearInterval
            )
        ).run()
        pass

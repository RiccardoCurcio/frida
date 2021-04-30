import sys
import pathlib
import os
import logging
from configparser import ConfigParser
from src.application.handler import HandlerFactory
from src.cliOption.config import Config
from src.bootstrap import Bootstrap
# from src.dependencies import Dependencies

# from src.backup import Backups
# from src.clear import Clear
# from src.list import List
# from src.database import DbConnection
# from src.help import Help
# from src.config import Config
# from src.only import Only
# from src.clearInterval import ClearInterval
# from src.overrideGateway import OverrideGateway
# from src.overrideClearGatewayExcept import OverrideClearGatewayExcept


# def main(logger, config):
#     dbs = DbConnection(logger)
#     if "--list" in sys.argv or "-l" in sys.argv:
#         listBk = List(logger)
#         listBk.run(
#             config,
#             Only.getOnlyService(sys.argv, logger, config)
#         )
#         exit(0)
#     if "--backup" in sys.argv or "-b" in sys.argv:
#         bk = Backups(logger)
#         OverrideGateway.setGateway(sys.argv, logger)
#         bk.run(
#             dbs,
#             config,
#             Only.getOnlyService(sys.argv, logger, config)
#         )
#     if "--clear" in sys.argv or "-c" in sys.argv:
#         ClearInterval.setClearInterval(sys.argv, logger)
#         OverrideGateway.setGateway(sys.argv, logger)
#         OverrideClearGatewayExcept.setClearGatewayExcept(sys.argv, logger)
#         clear = Clear(logger)
#         clear.run(
#             config,
#             Only.getOnlyService(sys.argv, logger, config)
#         )

def main(config: ConfigParser, logger: logging.Logger) -> None:
    HandlerFactory.run(config, logger, sys.argv)


if __name__ == '__main__':
    try:
        os.environ["FRIDA_PARENT_PATH"] = f'{pathlib.Path(__file__).parent.parent}'
        config = Config.setConfig(sys.argv)
        boot = Bootstrap(config)
        logger = boot.setLogger()
        main(config, logger)
    except KeyboardInterrupt:
        logger.info('Stopping script...')
        sys.exit(0)
    except Exception as e:
        logger.error(f'There was an error while starting process: {e}')
        sys.exit(1)

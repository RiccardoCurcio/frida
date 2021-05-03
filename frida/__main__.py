import sys
import pathlib
import os
import logging
from configparser import ConfigParser
from src.application.handler import HandlerFactory
from src.cliOption.config import Config
from src.bootstrap import Bootstrap


def main(config: ConfigParser, logger: logging.Logger) -> None:
    """[Main]

    Args:
        config (ConfigParser): [config parser]
        logger (logging.Logger): [logger]
    """
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

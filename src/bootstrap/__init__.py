import logging
import os
from datetime import datetime


class Bootstrap:
    def __init__(self, config):
        self.__config = config
        pass

    def setLogger(self) -> logging.Logger:
        try:
            if not os.path.exists(f'{os.getenv("FRIDA_PARENT_PATH")}/logs'):
                os.makedirs(f'{os.getenv("FRIDA_PARENT_PATH")}/logs')

            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    fmt='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            )

            now = datetime.now()
            log_name = now.strftime("%Y-%m-%d")

            logging.basicConfig(
                filename=f'{os.getenv("FRIDA_PARENT_PATH")}/logs/{log_name}_application.log',
                filemode='a',
                format='[%(asctime)s] %(levelname)s %(message)s'
            )
            logger = logging.getLogger('root')

            logger.setLevel(
                logging.getLevelName(
                    self.__config['DEFAULT'].get('LOGGING_LEVEL', 'INFO')
                )
            )
            logger.addHandler(handler)
        except Exception:
            os.exit(0)
        return logger

from logging import Logger
from subprocess import call, STDOUT
import os


class Dependencies:

    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        pass

    def check(self) -> None:
        try:
            DEVNULL = open(os.devnull, 'wb')
            if call(
                ['which', 'mysqldump'],
                stdout=DEVNULL,
                stderr=STDOUT
            ) == 0:
                self.__logger.info('mysqldump found')
            else:
                self.__logger.warning('mysqldump missing')

            if call(
                ['which', 'mongodump'],
                stdout=DEVNULL,
                stderr=STDOUT
            ) == 0:
                self.__logger.info('mongodump found')
            else:
                self.__logger.warning('mongodump missing')

            if call(
                ['which', 'tar'],
                stdout=DEVNULL,
                stderr=STDOUT
            ) == 0:
                self.__logger.info('tar found')
            else:
                self.__logger.warning('tar missing')
        finally:
            DEVNULL.close()

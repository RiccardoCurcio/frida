import os
import re
from logging import Logger


class ListMongoBk:
    def __init__(
        self,
        logger: Logger,
        dir: str
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        pass

    def run(
        self,
        service: str
    ) -> None:
        self.__listDirs(service)

    def __listDirs(self, service: str) -> None:
        try:
            path = f'{self.__dir_path}/{service}'

            print(f"\n[{service}]")
            if not os.path.exists(path):
                print(f" - Empity")
                return None

            r = re.compile('.*\.tgz$')
            for filename in list(filter(r.match, os.listdir(path))):
                print(f" - {path}/{filename}")
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo  FAILURE {e}"
            )

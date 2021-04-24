import os
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

            if not os.path.exists(path):
                self.__logger.error(
                    f"[{service}] Mongo path {path} not found"
                )
                return None

            print(f"\n[{service}]")
            for dir_name in os.listdir(path):
                print(f' - {path}/{dir_name}')
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo  FAILURE {e}"
            )

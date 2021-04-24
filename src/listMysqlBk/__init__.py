import os
import re


class ListMysqlBk:
    def __init__(
        self,
        logger,
        dir: str
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger

        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)

        if not os.path.exists(f'{os.getenv("PARENT_PATH")}/logs'):
            os.makedirs(f'{os.getenv("PARENT_PATH")}/logs')
        pass

    def run(
        self,
        service: str
    ) -> None:
        self.__listFiles(service)

    def __listFiles(self, service: str) -> None:
        try:
            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                self.__logger.error(
                    f"[{service}] Mysql Dumps path {path} not found"
                )
                return None

            r = re.compile('.*\.sql$')
            print(f"\n[{service}]")
            for filename in list(filter(r.match, os.listdir(path))):
                print(f" - {path}/{filename}")
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mysql Dumps list error: {e}"
            )

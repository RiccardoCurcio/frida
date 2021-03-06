import os
import json
from logging import Logger


class Mongo:
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
                print(f" - Empty")
                return None

            jsonStore = self.__loadJson(path)
            if len(jsonStore.keys()) == 0:
                print(f" - Empty")
                return None
            for key in jsonStore.keys():
                print(f"   {key}")
                for item in jsonStore[key]:
                    print(f"    - [{item['location']}] {item['key']}")
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo  FAILURE {e}"
            )

    def __loadJson(self, dirPath: str) -> dict:
        jsonStore = {}
        if os.path.exists(f'{dirPath}/.jsonStore.json'):
            with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                jsonStore = json.load(f)
        return jsonStore

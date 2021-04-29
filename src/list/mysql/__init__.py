import os
import json


class Mysql:
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
                f"[{service}] Mysql Dumps list error: {e}"
            )

    def __loadJson(self, dirPath: str) -> dict:
        jsonStore = {}
        if os.path.exists(f'{dirPath}/.jsonStore.json'):
            with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                jsonStore = json.load(f)
        return jsonStore

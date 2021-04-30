import os
import logging
from src.application.command.list import ListCommand
from src.process import Process


class ListProcess(Process):
    def __init__(self, logger: logging.Logger, command: ListCommand):
        self.__command = command
        self.__logger = logger
        super().__init__(self.__command.config, logger)

    def run(self):
        for service in self.__command.services:
            self.__listDirs(service)

    def __listDirs(self, service: str) -> None:
        try:
            print(f"[{service}]")
            if not os.path.exists(f'{self._fridaBackupDir}/{service}'):
                print(f" - Empty\n")
                return None

            jsonStore = self._loadJson(f'{self._fridaBackupDir}/{service}')

            if len(jsonStore.keys()) == 0:
                print(f" - Empty\n")
                return None
            for key in jsonStore.keys():
                print(f"   {key}")
                for item in jsonStore[key]:
                    print(f"    - [{item['location']}] {item['key']}")
            print("")
        except Exception as e:
            self.__logger.error(
                f"[{service}] list FAILURE {e}"
            )

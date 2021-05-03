import os
import logging
from src.application.command.check import CheckCommand
from src.process import Process


class CheckProcess(Process):
    def __init__(self, logger: logging.Logger, command: CheckCommand):
        self.__cmd = command
        self.__logger = logger
        super().__init__(self.__cmd.config, logger)

    def run(self):
        for service in self.__cmd.services:
            self.__checkService(service)

    def __checkService(self, service: str) -> None:
        try:
            # print(f"[{service}]")
            # if not os.path.exists(f'{self._fridaBackupDir}/{service}'):
            #     print(f" - Empty\n")
            #     return None

            # jsonStore = self._loadJson(f'{self._fridaBackupDir}/{service}')

            # if len(jsonStore.keys()) == 0:
            #     print(f" - Empty\n")
            #     return None
            # for key in jsonStore.keys():
            #     print(f"   {key}")
            #     for item in jsonStore[key]:
            #         print(f"    - [{item['location']}] {item['key']}")
            # print("")
            
            serviceType = self.__cmd.config[service].get('TYPE', None)

            if serviceType in self._dbTypeAllowed:
                if serviceType == 'mysql':
                    self._mysqlCheck(service)

                if serviceType == 'mongo':
                    self._mongoCheck(service)
        except Exception as e:
            self.__logger.error(
                f"[{service}] check FAILURE {e}"
            )

import os
import re
import json
from datetime import datetime
from logging import Logger
from src.gateway import Gateway


class Mongo:
    def __init__(
        self,
        logger: Logger,
        dir: str,
        date: datetime,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        self.__date = date
        self.__gateway = gateway.split(',') if gateway is not None else []
        pass

    def run(
        self,
        service: str
    ) -> None:
        self.__deleteDirs(service)
        self.__deleteLogs(service)

    def __deleteDirs(self, service: str) -> None:
        try:
            count = 0
            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                self.__logger.error(
                    f"[{service}] Mongo clear path {path} not found"
                )
                return None
            dictArchives = self.__loadJson(path)
            updatedArhive = {}
            for key in dictArchives.keys():
                if datetime.strptime(key.replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__date:
                    try:
                        updatedArhive.update({key: []})
                        for location in dictArchives[key]:
                            if location['location'] == 'frida':
                                if 'local' in self.__gateway:
                                    os.remove(f'{location["key"]}')
                                    self.__logger.info(
                                        f"[{service}] Mongo clear archive deleted -> {location['key']}"
                                    )
                                    count = count + 1
                                else:
                                    updatedArhive[key].append(location)
                            else:
                                # gateway
                                if location['location'] in self.__gateway:
                                    for gatewayPath in self.__gateway:
                                        if gatewayPath != 'local':
                                            if gatewayPath == location['location']:
                                                try:
                                                    g = Gateway.get(location['location'], self.__logger)
                                                    g.delete(location['key'])
                                                    count = count + 1
                                                except Exception as e:
                                                    self.__logger.error(f"Call gateway error {e}")
                                                    updatedArhive[key].append(location)
                                else:
                                    updatedArhive[key].append(location)
                            # count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[{service}] Mongo archive delete -> {key} error: {e}"
                        )
                else:
                    updatedArhive.update({key: dictArchives[key]})

            self.__updateJson(path, updatedArhive)
            self.__logger.info(
                f"[{service}] Mongo clear FINISH {count} archive deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo clear FAILURE {e}"
            )

    def __deleteLogs(self, service: str) -> None:
        try:
            count = 0
            path = f'{os.getenv("PARENT_PATH")}/logs'
            r = re.compile(f'^{service}_[\d]{{4}}-[\d]{{2}}-[\d]{{2}}_[\d]{{2}}:[\d]{{2}}:[\d]{{2}}\.log$')
            self.__logger.info(f"[{service}] Mongo log files clear START")
            for filename in list(filter(r.match, os.listdir(path))):
                file_noservice = filename.replace(f"{service}_", "")
                if datetime.strptime(file_noservice[:-4].replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__date:
                    try:
                        os.remove(f"{path}/{filename}")
                        self.__logger.info(
                            f"[{service}] delete -> {path}/{filename}"
                        )
                        count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[{service}] Mongo logs file delete -> {path}/{filename} error: {e}"
                        )
            self.__logger.info(
                f"[{service}] Mongo logs clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo logs clear  error: {e}"
            )

    def __loadJson(self, dirPath: str) -> dict:
        jsonStore = {}
        if os.path.exists(f'{dirPath}/.jsonStore.json'):
            with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                jsonStore = json.load(f)
        return jsonStore

    def __updateJson(self, dirPath: str, jsonStore) -> dict:
        jsonstoreClear = {}
        for key in jsonStore.keys():
            jsonstoreClear.update({key: jsonStore[key]}) if len(jsonStore[key]) > 0 else None 
        with open(f'{dirPath}/.jsonStore.json', 'w') as f:
            json.dump(jsonstoreClear, f)

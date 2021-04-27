import os
import json
import re
from datetime import datetime
from src.gateway import Gateway


class ClearMysqlBk:
    def __init__(
        self,
        logger,
        dir: str,
        date: datetime,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        self.__date = date
        self.__gateway = gateway.split(',') if gateway is not None else []

        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)

        if not os.path.exists(f'{os.getenv("PARENT_PATH")}/logs'):
            os.makedirs(f'{os.getenv("PARENT_PATH")}/logs')
        pass

    def run(
        self,
        service: str
    ) -> None:
        self.__deleteFiles(service)
        self.__deleteLogs(service)

    def __deleteFiles(self, service: str) -> None:
        try:
            count = 0
            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                self.__logger.error(
                    f"[{service}] Mysql Dumps clear path {path} not found"
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
                                os.remove(f'{location["key"]}')
                                self.__logger.info(
                                    f"[{service}] Mongo clear archive deleted -> {location['key']}"
                                )
                            else:
                                # gateway
                                if location['location'] in self.__gateway:
                                    for gatewayPath in self.__gateway:
                                        if gatewayPath == location['location']:
                                            g = Gateway.get(location['location'])
                                            g.delete(location['key'])
                                            self.__logger.info(
                                                f"[{service}] Mongo clear archive from gateway {location['location']} deleted -> {location['key']}"
                                            )
                                else:
                                    updatedArhive[key].append(location)
                            count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[{service}] Mongo archive delete -> {key} error: {e}"
                        )
                else:
                    updatedArhive.update({key: dictArchives[key]})

            self.__updateJson(path, updatedArhive)

            # r = re.compile('^[\d]{4}-[\d]{2}-[\d]{2}_[\d]{2}:[\d]{2}:[\d]{2}\.tgz$')
            # self.__logger.info(f"[{service}] Mysql Dumps clear START")
            # for filename in list(filter(r.match, os.listdir(path))):
            #     if datetime.strptime(filename[:-4].replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__date:
            #         try:
            #             os.remove(f"{path}/{filename}")
            #             self.__logger.info(
            #                 f"[{service}] delete -> {path}/{filename}"
            #             )
            #             # gateway
            #             for gatewayPath in self.__gateway:
            #                 g = Gateway.get(gatewayPath)
            #                 g.delete(f'{path}/{filename}')
            #             count = count + 1
            #         except Exception as e:
            #             self.__logger.error(
            #                 f"[{service}] Mysql archive delete -> {path}/{filename} error: {e}"
            #             )
            self.__logger.info(
                f"[{service}] Mysql archives clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mysql archives clear error: {e}"
            )

    def __deleteLogs(self, service: str) -> None:
        try:
            count = 0
            path = f'{os.getenv("PARENT_PATH")}/logs'
            r = re.compile(f'^{service}_[\d]{{4}}-[\d]{{2}}-[\d]{{2}}_[\d]{{2}}:[\d]{{2}}:[\d]{{2}}\.log$')
            self.__logger.info(f"[{service}] Mysql log files clear START")
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
                            f"[{service}] Mysql logs file delete -> {path}/{filename} error: {e}"
                        )
            self.__logger.info(
                f"[{service}] Mysql logs clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mysql logs clear error: {e}"
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

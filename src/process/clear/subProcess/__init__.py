import os
import re
import json
from datetime import datetime
from logging import Logger
from src.gateway import Gateway
from src.process import Process


class Clear:

    def __init__(
        self,
        process: Process,
        service: str,
        gateway: list,
        clearInterval: datetime
    ):
        self.__service = service
        self.__proc = process
        self._logger = self.__proc._logger
        self.__gateway = gateway if gateway is not None else []
        self.__backupPath = f'{self.__proc._fridaBackupDir}/{self.__service}'
        self.__clearInterval = clearInterval

    def run(self):
        content = self.__proc._loadJson(self.__backupPath)
        newJson = {}
        for key in content.keys():
            if datetime.strptime(
                key.replace("_", " "), "%Y-%m-%d %H:%M:%S"
            ) < self.__clearInterval:
                tmpJson = {key: []}
                for item in [({'l': 'local', 'k': g['key']} if g['location'] == 'frida' else {'l': g['location'], 'k': g['key']}) for g in content[key]]:
                    if item['l'] == 'local':
                        if os.path.exists(f'{item["k"]}'):
                            os.remove(f'{item["k"]}')
                            self._logger.info(f'[{self.__service}] local del {item["l"]} {item["k"]}')
                    else:
                        if item["l"] in self.__gateway:
                            try:
                                g = Gateway.get(item["l"], self._logger)
                                g.delete(item["k"])
                                self._logger.info(f'[{self.__service}] gateway del {item["l"]} {item["k"]}')
                            except Exception as e:
                                self._logger.error(f'[{self.__service}] gateway error {e}')
                                tmpJson[key].append({'location': item["l"], "key": item["k"]})
                        else:
                            tmpJson[key].append({'location': item["l"], "key": item["k"]})
                if len(tmpJson[key]) > 0:
                    newJson.update(tmpJson)
            else:
                newJson.update({key: content[key]})

        self.__proc._replaceJson(self.__backupPath, newJson)
        self.__clearLogs()

    def __clearLogs(self):
        r = re.compile(f'^{self.__service}_[\d]{{4}}-[\d]{{2}}-[\d]{{2}}_[\d]{{2}}:[\d]{{2}}:[\d]{{2}}\.log$')
        for filename in list(filter(r.match, os.listdir(f'{self.__proc._fridaParentPath}/logs/'))):
            file_noservice = filename.replace(f"{self.__service}_", "")
            if datetime.strptime(file_noservice[:-4].replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__clearInterval:
                if os.path.exists(f'{self.__proc._fridaParentPath}/logs/{filename}'):
                    os.remove(f'{self.__proc._fridaParentPath}/logs/{filename}')

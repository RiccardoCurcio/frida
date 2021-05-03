import os
import json
import logging
from src.database import DbConnection
from configparser import ConfigParser
from abc import ABC


class Process(ABC):
    def __init__(self, config: ConfigParser, logger: logging.Logger):
        self.__config = config
        self._logger = logger
        self._fridaParentPath = os.getenv('FRIDA_PARENT_PATH')
        self._fridaBackupDir = self.__config['DEFAULT'].get(
            'DIR',
            f'{self._fridaParentPath}/backups'
        )
        self._dbTypeAllowed = ['mysql', 'mongo']
        self._devMode = self.__config['DEFAULT'].getboolean("DEV_MODE", False)
        pass

    def _loadJson(self, dirPath: str) -> dict:
        try:
            jsonStore = {}
            if os.path.exists(f'{dirPath}/.jsonStore.json'):
                with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                    jsonStore = json.load(f)
            return jsonStore
        except Exception as e:
            self._logger.error(
                f"[{dirPath}] json load error {e}"
            )

    def _replaceJson(self, dirPath: str, content: dict):
        with open(f'{dirPath}/.jsonStore.json', 'w') as f:
            json.dump(content, f)
            f.close()

    def _mysqlCheck(self, service: str):
        try:
            if self._devMode is False:
                dbs = DbConnection(self._logger)
                if dbs.mysqlconnect(
                    self.__config[service].get('DB_HOST', None),
                    self.__config[service].get('DB_PORT', None),
                    self.__config[service].get('DB_DATABASE', None),
                    self.__config[service].get('DB_USERNAME', None),
                    self.__config[service].get('DB_PASSWORD', None),
                    self.__config[service].get('DB_CHARSET', 'utf8')
                ):
                    self._logger.info(
                        f'[{service}] Mysql connection SUCCESS'
                    )
                    return True
                self._logger.error(
                    f"[{service}] Mysql Authentication FAILURE"
                )
                self._logger.info(
                    f"[{service}] SKIP"
                )
                return False
            self._logger.debug(f"[{service}] DEV MODE ENABLE")
            return True
        except Exception as e:
            self._logger.error(
                f"[{service}] Mysql Authentication FAILURE {e}"
            )
            self._logger.info(
                f"[{service}] SKIP"
            )

    def _mongoCheck(self, service: str):
        try:
            if self._devMode is False:
                dbs = DbConnection(self._logger)
                if dbs.mongoconnect(
                    self.__config[service].get('DB_HOST', None),
                    self.__config[service].get('DB_PORT', None),
                    self.__config[service].get('DB_DATABASE', None),
                    self.__config[service].get('DB_USERNAME', None),
                    self.__config[service].get('DB_PASSWORD', None),
                    self.__config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                ):
                    self._logger.info(
                        f'[{service}] Mongo connection SUCCESS'
                    )
                    return True
                self._logger.error(
                    f"[{service}] Mongo Authentication FAILURE"
                )
                self._logger.info(
                    f"[{service}] SKIP"
                )
                return False
            self._logger.debug(f"DEV MODE ENABLE")
            return True
        except Exception as e:
            self._logger.error(
                f"[{service}] Mongo Authentication FAILURE {e}"
            )
            self._logger.info(
                f"[{service}] SKIP"
            )

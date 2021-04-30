import os
import json
import logging
from src.database import DbConnection
from configparser import ConfigParser
from abc import ABC


class Process(ABC):
    def __init__(self, config: ConfigParser, logger: logging.Logger):
        self.__config = config
        self.__logger = logger
        self._fridaParentPath = os.getenv('FRIDA_PARENT_PATH')
        self._fridaBackupDir = self.__config['DEFAULT'].get(
            'DIR',
            f'{self._fridaParentPath}/backups'
        )
        pass

    def _loadJson(self, dirPath: str) -> dict:
        try:
            jsonStore = {}
            if os.path.exists(f'{dirPath}/.jsonStore.json'):
                with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                    jsonStore = json.load(f)
            return jsonStore
        except Exception as e:
            self.__logger.error(
                f"[{dirPath}] json load error {e}"
            )

    def _mysqlCheck(self, service: str):
        dbs = DbConnection(self.__logger)
        if dbs.mysqlconnect(
            self.__config[service].get('DB_HOST', None),
            self.__config[service].get('DB_PORT', None),
            self.__config[service].get('DB_DATABASE', None),
            self.__config[service].get('DB_USERNAME', None),
            self.__config[service].get('DB_PASSWORD', None),
            self.__config[service].get('DB_CHARSET', 'utf8')
        ):
            self.__logger.info(
                f'[{service}] Mysql connection SUCCESS'
            )
            return True
        self.__logger.error(
            f"[{service}] Mysql Authentication FAILURE"
        )
        return False

    def _mongoCheck(self, service: str):
        dbs = DbConnection(self.__logger)
        if dbs.mongoconnect(
            self.__config[service].get('DB_HOST', None),
            self.__config[service].get('DB_PORT', None),
            self.__config[service].get('DB_DATABASE', None),
            self.__config[service].get('DB_USERNAME', None),
            self.__config[service].get('DB_PASSWORD', None),
            self.__config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
        ):
            self.__logger.info(
                f'[{service}] Mongo connection SUCCESS'
            )
            return True
        self.__logger.info(
            f"[{service}] Mongo Authentication FAILURE"
        )
        return False

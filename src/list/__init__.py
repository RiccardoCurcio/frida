import os
from configparser import ConfigParser
from src.database import DbConnection
from src.list.mysql import Mysql
from src.list.mongo import Mongo


class List:

    def __init__(self, logger):
        self.__logger = logger
        pass

    def run(self, dbs: DbConnection, config: ConfigParser, services: list) -> None:
        default_dir = config['DEFAULT'].get(
            'DIR',
            f'{os.getenv("PARENT_PATH")}/backups'
        )

        for service in services:
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                if config[service].get('TYPE', None) == 'mysql':
                    if dbs.mysqlconnect(
                        config[service].get('DB_HOST', None),
                        config[service].get('DB_PORT', None),
                        config[service].get('DB_DATABASE', None),
                        config[service].get('DB_USERNAME', None),
                        config[service].get('DB_PASSWORD', None),
                        config[service].get('DB_CHARSET', 'utf8')
                    ):
                        self.__logger.info(
                            f'[{service}] Mysql connection SUCCESS'
                        )
                    else:
                        self.__logger.error(
                            f'[{service}] Mysql connection FAILLURE'
                        )
                    listMysql = Mysql(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listMysql.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    if dbs.mongoconnect(
                        config[service].get('DB_HOST', None),
                        config[service].get('DB_PORT', None),
                        config[service].get('DB_DATABASE', None),
                        config[service].get('DB_USERNAME', None),
                        config[service].get('DB_PASSWORD', None),
                        config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                    ):
                        self.__logger.info(
                            f'[{service}] Mongo connection SUCCESS'
                        )
                    else:
                        self.__logger.error(
                            f'[{service}] Mongo connection FAILURE'
                        )
                    listMongo = Mongo(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listMongo.run(service)

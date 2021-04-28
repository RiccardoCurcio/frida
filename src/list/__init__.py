import os
from configparser import ConfigParser
from src.list.mysql import Mysql
from src.list.mongo import Mongo


class List:

    def __init__(self, logger):
        self.__logger = logger
        pass

    def run(self, config: ConfigParser, services: list) -> None:
        default_dir = config['DEFAULT'].get(
            'DIR',
            f'{os.getenv("PARENT_PATH")}/backups'
        )

        for service in services:
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                if config[service].get('TYPE', None) == 'mysql':
                    listMysql = Mysql(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listMysql.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    listMongo = Mongo(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listMongo.run(service)

import os
from configparser import ConfigParser
from src.listMysqlBk import ListMysqlBk
from src.listMongoBk import ListMongoBk


class ListBk:

    def __init__(self, logger):
        self.__logger = logger
        pass

    def run(self, config: ConfigParser, services: list):
        default_dir = config['DEFAULT'].get(
            'DIR',
            f'{os.getenv("PARENT_PATH")}/backups'
        )

        for service in services:
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                if config[service].get('TYPE', None) == 'mysql':
                    listBk = ListMysqlBk(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listBk.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    listBk = ListMongoBk(
                        self.__logger,
                        config[service].get('DIR', default_dir)
                    )
                    listBk.run(service)

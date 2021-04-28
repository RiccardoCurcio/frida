import os
from src.backup.mysql import Mysql
from src.backup.mongo import Mongo
from src.database import DbConnection
from configparser import ConfigParser
from logging import Logger


class Backups:

    def __init__(self, logger: Logger) -> None:
        """[init Backup]

        Args:
            logger (Logger): [logger]
        """
        self.__logger = logger
        pass

    def run(self, dbs: DbConnection, config: ConfigParser, services: list):
        """[Run backup]

        Args:
            dbs (DbConnection): [databases connections]
            config (ConfigParser): [config data]
            services (list): [list of services]
        """
        default_dir = config['DEFAULT'].get(
            'DIR',
            f'{os.getenv("PARENT_PATH")}/backups'
        )

        default_gateway = config['DEFAULT'].get(
            'GATEWAY',
            None
        )

        if not os.path.exists(default_dir):
            os.makedirs(default_dir)

        for s in services:
            sType = config[s].get('TYPE', None)
            if sType in ['mysql', 'mongo']:
                if sType == 'mysql':
                    self.__runMysql(dbs, config, s, default_dir)

                if sType == 'mongo':
                    self.__runMongo(dbs, config, s, default_dir)
            else:
                self.__logger.error(
                    f"[service={s}] [type={sType}] No type allowed FAILURE"
                )

    def __runMysql(
        self,
        dbs: DbConnection,
        config: ConfigParser,
        service: str,
        default_dir: str,
        default_gateway: str = None
    ):
        """[Run backup mysql service]

        Args:
            dbs (DbConnection): [databases connections]
            config (ConfigParser): [config data]
            service (str): [service name]
            default_dir (str): [dir for backup]
        """
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
            mysql = Mysql(
                self.__logger,
                config[service].get('DIR', default_dir),
                config[service].get('GATEWAY', default_gateway)
            )
            mysql.run(
                service,
                config[service].get('DB_HOST', None),
                config[service].get('DB_PORT', None),
                config[service].get('DB_DATABASE', None),
                config[service].get('DB_USERNAME', None),
                config[service].get('DB_PASSWORD', None)
            )
        else:
            self.__logger.error(
                f"[{service}] Mysql Authentication FAILURE"
            )

    def __runMongo(
        self,
        dbs: DbConnection,
        config: ConfigParser,
        service: str,
        default_dir: str,
        default_gateway: str = None
    ):
        """[Run mongo backup]

        Args:
            dbs (DbConnection): [databases connections]
            config (ConfigParser): [config data]
            service (str): [service name]
            default_dir (str): [dir for backup]
        """
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
            mongo = Mongo(
                self.__logger,
                config[service].get('DIR', default_dir),
                config[service].get('GATEWAY', default_gateway)
            )
            mongo.run(
                service,
                config[service].get('DB_HOST', None),
                config[service].get('DB_PORT', None),
                config[service].get('DB_DATABASE', None),
                config[service].get('DB_USERNAME', None),
                config[service].get('DB_PASSWORD', None)
            )
        else:
            self.__logger.info(
                f"[{service}] Mongo Authentication FAILURE"
            )

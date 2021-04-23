import os
from src.mysqlBk import MysqlBk
from src.mongoBk import MongoBk
from src.database import DbConnection
from configparser import ConfigParser

class Backups:
    
    def __init__(self, logger):
        self.__logger = logger
        pass
    
    def run(self, dbs:DbConnection, config:ConfigParser):
        default_dir = config['DEFAULT'].get('DIR', f'{os.getenv("PARENT_PATH")}/backups')
        
        if not os.path.exists(default_dir):
            os.makedirs(default_dir)
        
        services = config.sections()
        
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
                        self.__logger.info(f'[{service}] Mysql connection SUCCESS')
                        mysql = MysqlBk(self.__logger, config[service].get('DIR', default_dir))
                        mysql.run(
                            service,
                            config[service].get('DB_HOST', None),
                            config[service].get('DB_PORT', None),
                            config[service].get('DB_DATABASE', None),
                            config[service].get('DB_USERNAME', None),
                            config[service].get('DB_PASSWORD', None)
                        )
                    else:
                        self.__logger.error(f"[{service}] Mysql Authentication FAILURE")

                if config[service].get('TYPE', None) == 'mongo':
                    if dbs.mongoconnect(
                        config[service].get('DB_HOST', None),
                        config[service].get('DB_PORT', None),
                        config[service].get('DB_DATABASE', None),
                        config[service].get('DB_USERNAME', None),
                        config[service].get('DB_PASSWORD', None),
                        config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                    ):
                        self.__logger.info(f'[{service}] Mongo connection SUCCESS')
                        mongo = MongoBk(self.__logger, config[service].get('DIR', default_dir))
                        mongo.run(
                            service,
                            config[service].get('DB_HOST', None),
                            config[service].get('DB_PORT', None),
                            config[service].get('DB_DATABASE', None),
                            config[service].get('DB_USERNAME', None),
                            config[service].get('DB_PASSWORD', None)
                        )
                    else:
                        self.__logger.info(f"[{service}] Mongo Authentication FAILURE")
            else:
                self.__logger.error(f"[service={service}] [type={config[service].get('TYPE', None)}] No type allowed FAILURE")
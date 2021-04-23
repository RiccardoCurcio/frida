import os
from src.mysqlBk import MysqlBk
from src.mongoBk import MongoBk
from src.database import DbConnection
from configparser import ConfigParser

class Backups:
    
    def __init__(self):
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
                        print(f'[{service}] Mysql connection \033[92mSUCCESS\033[0m')
                        mysql = MysqlBk(config[service].get('DIR', default_dir))
                        mysql.run(
                            service,
                            config[service].get('DB_HOST', None),
                            config[service].get('DB_PORT', None),
                            config[service].get('DB_DATABASE', None),
                            config[service].get('DB_USERNAME', None),
                            config[service].get('DB_PASSWORD', None)
                        )
                    else:
                        print(f"[{service}] Mysql Authentication \033[91mFAILURE\033[0m")

                if config[service].get('TYPE', None) == 'mongo':
                    if dbs.mongoconnect(
                        config[service].get('DB_HOST', None),
                        config[service].get('DB_PORT', None),
                        config[service].get('DB_DATABASE', None),
                        config[service].get('DB_USERNAME', None),
                        config[service].get('DB_PASSWORD', None),
                        config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                    ):
                        print(f'[{service}] Mongo connection \033[92mSUCCESS\033[0m')
                        mongo = MongoBk(config[service].get('DIR', default_dir))
                        mongo.run(
                            service,
                            config[service].get('DB_HOST', None),
                            config[service].get('DB_PORT', None),
                            config[service].get('DB_DATABASE', None),
                            config[service].get('DB_USERNAME', None),
                            config[service].get('DB_PASSWORD', None)
                        )
                    else:
                        print(f"[{service}] Mongo Authentication \033[91mFAILURE\033[0m")
            else:
                print(f"[service={service}] [type={config[service].get('TYPE', None)}] No type allowed \033[91mFAILURE\033[0m")
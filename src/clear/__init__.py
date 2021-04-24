import os
import re
from datetime import datetime, timedelta
from configparser import ConfigParser
from src.clearMysqlBk import ClearMysqlBk
from src.clearMongoBk import ClearMongoBk


class Clear:

    def __init__(self, logger):
        self.__logger = logger
        pass

    def run(self, config: ConfigParser, services: list):
        default_dir = config['DEFAULT'].get(
            'DIR',
            f'{os.getenv("PARENT_PATH")}/backups'
        )

        diffTime = config['DEFAULT'].get(
            'CLEAR',
            '365'
        )
        date = datetime.now() - timedelta(days=int(diffTime))

        for service in services:
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                if config[service].get('TYPE', None) == 'mysql':
                    clear = ClearMysqlBk(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date
                    )
                    clear.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    clear = ClearMongoBk(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date
                    )
                    clear.run(service)
        self.__clearLogs(date)

    def __clearLogs(self, date: datetime):
        try:
            count = 0
            path = f'{os.getenv("PARENT_PATH")}/logs'
            r = re.compile(f'.*\_application.log$')
            self.__logger.info(f"Application log files clear START")
            for filename in list(filter(r.match, os.listdir(path))):
                file_noservice = filename.replace(f"_application", "")
                if datetime.strptime(file_noservice[:-4].replace("_", " "), "%Y-%m-%d") < date:
                    try:
                        os.remove(f"{path}/{filename}")
                        self.__logger.info(
                            f"Application delete -> {path}/{filename}"
                        )
                        count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"Application logs file delete -> {path}/{filename} error: {e}"
                        )
            self.__logger.info(
                f"Application logs clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"Application logs clear error: {e}"
            )

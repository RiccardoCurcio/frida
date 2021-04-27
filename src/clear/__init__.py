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
            'CLEAR_INTERVAL',
            '365'
        )

        for service in services:
            serviceDiffTime = config[service].get('CLEAR_INTERVAL', diffTime)
            date = datetime.now() - timedelta(days=int(serviceDiffTime))
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                if config[service].get('TYPE', None) == 'mysql':
                    clear = ClearMysqlBk(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date,
                        config[service].get('GATEWAY', None) if config[service].getboolean('CLEAR_GATEWAY', False) is True else None
                    )
                    clear.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    clear = ClearMongoBk(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date,
                        config[service].get('GATEWAY', None) if config[service].getboolean('CLEAR_GATEWAY', False) is True else None
                    )
                    clear.run(service)

        date = datetime.now() - timedelta(days=int(diffTime))
        self.__clearLogs(date)

    def __clearLogs(self, date: datetime):
        try:
            count = 0
            path = f'{os.getenv("PARENT_PATH")}/logs'
            r = re.compile('^[\d]{4}-[\d]{2}-[\d]{2}_application.log$')
            self.__logger.info(f"[frida] log files clear START")
            for filename in list(filter(r.match, os.listdir(path))):
                file_noservice = filename.replace(f"_application", "")
                if datetime.strptime(file_noservice[:-4].replace("_", " "), "%Y-%m-%d") < date:
                    try:
                        os.remove(f"{path}/{filename}")
                        self.__logger.info(
                            f"[frida] delete -> {path}/{filename}"
                        )
                        count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[frida] logs file delete -> {path}/{filename} error: {e}"
                        )
            self.__logger.info(
                f"[frida] logs clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[frida] logs clear error: {e}"
            )

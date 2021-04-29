import os
import re
from datetime import datetime, timedelta
from configparser import ConfigParser
from src.clear.mysql import Mysql
from src.clear.mongo import Mongo


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
            
            # Override clear interval
            if os.getenv('FRIDA_CLEAR_INTERVAL', None) is not None:
                serviceDiffTime = os.getenv('FRIDA_CLEAR_INTERVAL', None)
                
            self.__logger.debug(f'[{service}] CLEAR_INTERVAL {serviceDiffTime}')
            
            date = datetime.now() - timedelta(days=int(serviceDiffTime))
            if config[service].get('TYPE', None) in ['mysql', 'mongo']:
                gatewaysList = config[service].get('GATEWAY', config['DEFAULT'].get('GATEWAY', 'local'))
                
                # Override gateway
                if os.getenv('FRIDA_OVERRIDE_GATEWAY', None) is not None:
                    gatewaysList =  os.getenv('FRIDA_OVERRIDE_GATEWAY', None)
                
                gatewayExcept = config[service].get('CLEAR_GATEWAY_EXCEPT', '')
                
                # Override clear gateway exception
                if os.getenv('FRIDA_OVERRIDE_CLEAR_GATEWAY_EXCEPT', None) is not None:
                    if os.getenv('FRIDA_OVERRIDE_CLEAR_GATEWAY_EXCEPT', None) == '--RESET--':
                        gatewayExcept = ''
                    gatewayExcept = os.getenv('FRIDA_OVERRIDE_CLEAR_GATEWAY_EXCEPT', None)
                
                if config[service].get('TYPE', None) == 'mysql':
                    clear = Mysql(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date,
                        ','.join([x for x in gatewaysList.split(',') if (x not in gatewayExcept.split(','))])
                    )
                    clear.run(service)
                if config[service].get('TYPE', None) == 'mongo':
                    clear = Mongo(
                        self.__logger,
                        config[service].get('DIR', default_dir),
                        date,
                        ','.join([x for x in gatewaysList.split(',') if (x not in gatewayExcept.split(','))])
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

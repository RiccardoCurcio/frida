import logging
import os
import re
from src.application.command.clear import ClearCommand
from src.process import Process
from datetime import datetime, timedelta
from src.process.clear.subProcess import Clear as ClearSubProcess


class ClearProcess(Process):
    def __init__(self, logger: logging.Logger, command: ClearCommand):
        self.__command = command
        self.__logger = logger
        super().__init__(self.__command.config, logger)

    def run(self):
        diffTime = self.__command.config['DEFAULT'].get(
            'CLEAR_INTERVAL',
            '365'
        )

        for service in self.__command.services:
            serviceDiffTime = self.__command.config[service].get('CLEAR_INTERVAL', diffTime)
            if self.__command.overrideClearInterval is not None:
                serviceDiffTime = self.__command.overrideClearInterval

            self.__logger.debug(f'[{service}] CLEAR_INTERVAL {serviceDiffTime}')
            
            date = datetime.now() - timedelta(days=int(serviceDiffTime))
            if self.__command.config[service].get('TYPE', None) in ['mysql', 'mongo']:
                gatewaysList = self.__command.config[service].get(
                    'GATEWAY',
                    self.__command.config['DEFAULT'].get(
                        'GATEWAY',
                        'local'
                    )
                ).split(',')

                if self.__command.overrideGateway:
                    gatewaysList = self.__command.overrideGateway

                gatewayExcept = self.__command.config[service].get('CLEAR_GATEWAY_EXCEPT', '')
                
                # Override clear gateway exception
                if self.__command.overrideClearGatewayExcept is not None:
                    if self.__command.overrideClearGatewayExcept == '--RESET--':
                        gatewayExcept = ''
                    else:
                        gatewayExcept = self.__command.overrideClearGatewayExcept
                ClearSubProcess(
                    self.__logger,
                    self.__command.config[service].get(
                        'DIR',
                        self._fridaBackupDir
                    ),
                    self._fridaParentPath,
                    date,
                    ','.join([x for x in gatewaysList if (x not in gatewayExcept.split(','))])
                ).run(service)

        date = datetime.now() - timedelta(days=int(diffTime))
        self.__clearLogs(date)

    def __clearLogs(self, date: datetime):
        try:
            count = 0
            path = f'{self._fridaParentPath}/logs'
            r = re.compile('^[\\d]{4}-[\\d]{2}-[\\d]{2}_application.log$')
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
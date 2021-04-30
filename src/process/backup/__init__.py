import logging
import os
from src.application.command.backup import BackupCommand
from src.process import Process
from src.process.backup.subProcess.mysql import Mysql
from src.process.backup.subProcess.mongo import Mongo


class BackupProcess(Process):
    def __init__(self, logger: logging.Logger, command: BackupCommand):
        self.__command = command
        self.__logger = logger
        super().__init__(self.__command.config, logger)

    def run(self):
        backupDir = self._fridaBackupDir

        if not os.path.exists(backupDir):
            os.makedirs(backupDir)

        for service in self.__command.services:
            serviceType = self.__command.config[service].get('TYPE', None)

            gateway = self.__command.config[service].get(
                    'GATEWAY',
                    self.__command.config['DEFAULT'].get(
                        'GATEWAY',
                        'local'
                    )
                ).split(',')

            if self.__command.overrideGateway:
                gateway = self.__command.overrideGateway

            if serviceType in ['mysql', 'mongo']:
                if serviceType == 'mysql' and self._mysqlCheck(service):
                    Mysql(
                        self.__logger,
                        backupDir,
                        self._fridaParentPath,
                        gateway
                    ).run(
                        service,
                        self.__command.config[service].get('DB_HOST', None),
                        self.__command.config[service].get('DB_PORT', None),
                        self.__command.config[service].get('DB_DATABASE', None),
                        self.__command.config[service].get('DB_USERNAME', None),
                        self.__command.config[service].get('DB_PASSWORD', None)
                    )

                if serviceType == 'mongo' and self._mongoCheck(service):
                    Mongo(
                        self.__logger,
                        backupDir,
                        self._fridaParentPath,
                        gateway
                    ).run(
                        service,
                        self.__command.config[service].get('DB_HOST', None),
                        self.__command.config[service].get('DB_PORT', None),
                        self.__command.config[service].get('DB_DATABASE', None),
                        self.__command.config[service].get('DB_USERNAME', None),
                        self.__command.config[service].get('DB_PASSWORD', None),
                        self.__command.config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                    )
            else:
                self.__logger.error(
                    f"[service={service}] [type={serviceType}] No type allowed FAILURE"
                )

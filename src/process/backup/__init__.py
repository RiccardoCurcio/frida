import logging
import os
from src.application.command.backup import BackupCommand
from src.process import Process
from src.process.backup.subProcess.mysql import Mysql
from src.process.backup.subProcess.mongo import Mongo


class BackupProcess(Process):
    def __init__(self, logger: logging.Logger, cmd: BackupCommand):
        self._cmd = cmd
        super().__init__(self._cmd.config, logger)

    def run(self):
        if not os.path.exists(self._fridaBackupDir):
            os.makedirs(self._fridaBackupDir)

        for service in self._cmd.services:
            serviceType = self._cmd.config[service].get('TYPE', None)

            gateway = self._cmd.config[service].get(
                    'GATEWAY',
                    self._cmd.config['DEFAULT'].get(
                        'GATEWAY',
                        'local'
                    )
                ).split(',')

            if self._cmd.overrideGateway:
                gateway = self._cmd.overrideGateway

            if serviceType in self._dbTypeAllowed:
                if serviceType == 'mysql' and self._mysqlCheck(service):
                    self._logger.debug(f"[{service}] Call subprocess mysql bk")
                    
                    Mysql(self, service, gateway).run()
                    # Mysql(
                    #     self._logger,
                    #     self._fridaBackupDir,
                    #     self._fridaParentPath,
                    #     service,
                    #     gateway
                    # ).run(
                    #     self._cmd.config[service].get('DB_HOST', None),
                    #     self._cmd.config[service].get('DB_PORT', None),
                    #     self._cmd.config[service].get('DB_DATABASE', None),
                    #     self._cmd.config[service].get('DB_USERNAME', None),
                    #     self._cmd.config[service].get('DB_PASSWORD', None)
                    # )

                if serviceType == 'mongo' and self._mongoCheck(service):
                    self._logger.debug(f"[{service}] Call subprocess mongo bk")
                    Mongo(self, service, gateway).run()
                    # Mongo(
                    #     self._logger,
                    #     self._fridaBackupDir,
                    #     self._fridaParentPath,
                    #     gateway
                    # ).run(
                    #     service,
                    #     self._cmd.config[service].get('DB_HOST', None),
                    #     self._cmd.config[service].get('DB_PORT', None),
                    #     self._cmd.config[service].get('DB_DATABASE', None),
                    #     self._cmd.config[service].get('DB_USERNAME', None),
                    #     self._cmd.config[service].get('DB_PASSWORD', None),
                    #     self._cmd.config[service].get('DB_MECHANISM', 'SCRAM-SHA-256')
                    # )
            else:
                self._logger.error(
                    f"[service={service}] [type={serviceType}] No type allowed FAILURE"
                )

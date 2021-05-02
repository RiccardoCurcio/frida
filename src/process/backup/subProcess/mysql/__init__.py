from subprocess import run as runProcess, STDOUT
import os
import typing
from datetime import datetime
from src.gateway import Gateway
from src.process import Process


class Mysql:

    def __init__(self, process: Process, service: str, gateway: list) -> None:
        self.__service = service
        self.__proc = process
        self._logger = self.__proc._logger
        self.__gateway = gateway if gateway is not None else []
        self.__localPersistence = False
        self.__backupPath = f'{self.__proc._fridaBackupDir}/{self.__service}'
        self.__dumpName = (datetime.now()).strftime("%Y-%m-%d_%H:%M:%S")
        self.__dumpPath = f'{self.__backupPath}/{self.__dumpName}'

        if 'local' in self.__gateway:
            self.__localPersistence = True
            self.__gateway.remove('local')

        None if os.path.exists(self.__proc._fridaBackupDir) else os.makedirs(
            self.__proc._fridaBackupDir)
        None if os.path.exists(self.__backupPath) else os.makedirs(
            self.__backupPath)
        None if os.path.exists(
            f'{self.__proc._fridaParentPath}/logs'
            ) else os.makedirs(f'{self.__proc._fridaParentPath}/logs')

        self.__logFile = f"""{
                self.__proc._fridaParentPath
            }/logs/{
                self.__service
            }_{
                self.__dumpName
            }.log"""

        self.__dCmd = [
            f'mysqldump',
            f"-h{self.__proc._cmd.config[self.__service].get('DB_HOST', None)}",
            f"-P{self.__proc._cmd.config[self.__service].get('DB_PORT', None)}",
            f"-u{self.__proc._cmd.config[self.__service].get('DB_USERNAME', None)}",
            f"-p{self.__proc._cmd.config[self.__service].get('DB_PASSWORD', None)}",
            f"{self.__proc._cmd.config[self.__service].get('DB_DATABASE', None)}"
        ]

    def run(self) -> None:
        """[Run mysql dump process]
        """
        try:
            # create dump - local (.sql)
            dumpFile = self.__createDump(self.__dumpPath, self.__dCmd)

            Mysql.ServiceLogger.info(
                self.__logFile,
                self.__service,
                f"Dump file {dumpFile} CREATED"
            )

            # create archive from local dump
            archiveFile = self.__createArchive(dumpFile)

            Mysql.ServiceLogger.info(
                self.__logFile,
                self.__service,
                f"Archive {archiveFile} CREATED"
            )

            # remove local dump
            self.__removeDump(dumpFile)
            Mysql.ServiceLogger.info(
                self.__logFile,
                self.__service,
                f"Dump file {dumpFile} REMOVED"
            )

            # send gateway
            locations = [] + self.__callGateway(
                archiveFile) if archiveFile else []

            # if persistance is false remove local archive
            if self.__localPersistence:
                locations = locations + [
                    {
                        'location': 'frida',
                        'key': archiveFile
                    }
                ]
            else:
                self.__removeDump(archiveFile)
                Mysql.ServiceLogger.info(
                    self.__logFile,
                    self.__service,
                    f"Local archive {archiveFile} REMOVED"
                )

            # create or update a jsonStore.json
            self.__updateJsonStore(locations)
            Mysql.ServiceLogger.info(
                    self.__logFile,
                    self.__service,
                    f".jsonStore.json UPDATED"
                )
        except Exception as e:
            Mysql.ServiceLogger.error(
                    self.__logFile,
                    self.__service,
                    f"Error dump {e}"
                )

    def __createDump(self, dumpPath: str, cmd: list) -> str:
        """[Create dump file]

        Args:
            dumpPath (str): [description]
            cmd (list): [description]

        Returns:
            str: [description]
        """
        try:
            self._logger.debug(
                f"[{self.__service}] DUMP COMMAND {self.__dCmd}")
            self._logger.info(f"[{self.__service}] create dump START")

            if not self.__proc._devMode:
                with open(self.__logFile, 'a') as f:
                    runProcess(
                        cmd,
                        stderr=f,
                        stdout=open(f'{dumpPath}.sql', 'w'),
                        universal_newlines=True
                    )
            else:
                self._logger.debug(f"[{self.__service}] DEV MODE TRUE")
                with open(f'{dumpPath}.sql', 'w') as devModeFile:
                    devModeFile.write("DEV-MODE")

            self._logger.info(f"[{self.__service}] create dump FINSH")
            return f'{dumpPath}.sql'
        except Exception as e:
            self._logger.error(f"[{self.__service}] create dump FAILURE {e}")
            raise Exception(f"__createDump {e}")

    def __removeDump(self, dumpFile: str) -> None:
        """[Remove file]

        Args:
            dumpFile (str): [description]
        """
        try:
            self._logger.info(
                f"[{self.__service}] remove {dumpFile} file START")
            if os.path.exists(f'{dumpFile}'):
                os.remove(f'{dumpFile}')
            self._logger.info(
                f"[{self.__service}] remove {dumpFile} file FINISH")
        except Exception as e:
            self._logger.error(
                f"[{self.__service}] remove {dumpFile} file FAILURE {e}")
            raise Exception(f"__removeDump {e}")

    def __createArchive(self, dumpFile: str) -> typing.Union[str, None]:
        """[Create archive .tgz]

        Args:
            dumpFile (str): [description]

        Returns:
            typing.Union[str, None]: [description]
        """
        try:
            self._logger.info(f"[{self.__service}] create archive START")
            DEVNULL = open(os.devnull, 'wb')
            cmd = [
                'tar',
                '-czvf',
                f'{dumpFile.replace("sql", "tgz")}',
                '-C',
                f'{self.__backupPath}',
                f'{self.__dumpName}.sql'
            ]
            runProcess(
                cmd,
                stdout=DEVNULL,
                stderr=STDOUT,
                universal_newlines=True
            )
            self._logger.info(f"[{self.__service}] create archive FINSH")
            return dumpFile.replace("sql", "tgz")
        except Exception as e:
            self._logger.error(
                f"[{self.__service}] archive create FAILURE {e}")
            raise Exception(f"__createArchive {e}")
        finally:
            DEVNULL.close()
        return None

    def __callGateway(self, archive: str) -> list:
        """[Call gateways]

        Args:
            archive (str): [description]

        Raises:
            Exception: [description]

        Returns:
            list: [description]
        """
        locations = []

        for gatewayPath in self.__gateway:
            try:
                g = Gateway.get(gatewayPath, self._logger)
                key = g.send(archive)
                if key is None:
                    raise Exception("None key from gateway")
                locations.append({'location': gatewayPath, 'key': key})
            except Exception as e:
                self._logger.error(f"Call gateway error {e}")
                raise Exception(f"__callGateway {e}")
        return locations

    def __updateJsonStore(self,  locations: list) -> None:
        """[Update jsonStore file]

        Args:
            locations (list): [description]

        Raises:
            Exception: [description]
        """
        try:
            if len(locations) > 0:
                content = self.__proc._loadJson(self.__backupPath)
                content.update({self.__dumpName: locations})
                self.__proc._replaceJson(self.__backupPath, content)
        except Exception as e:
            self._logger.error(f".jsonStore.json error {e}")
            raise Exception(f"__updateJsonStore {e}")

    class ServiceLogger:

        @classmethod
        def info(cls, logFile, service, msg=""):
            with open(logFile, 'a') as f:
                f.write(
                    f"""[{
                        (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                        }] INFO {__name__} {service} {msg}\n""")
                f.close()

        @classmethod
        def error(cls, logFile, service, msg=""):
            with open(logFile, 'a') as f:
                f.write(f"""[{
                    (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                    }] ERROR {__name__} {service} {msg}\n""")
                f.close()

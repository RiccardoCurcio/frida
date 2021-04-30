import os
import json
from subprocess import run as runProcess, STDOUT
from datetime import datetime
from logging import Logger
from shutil import rmtree
from src.gateway import Gateway


class Mongo:
    def __init__(
        self,
        logger: Logger,
        dir: str,
        parentPath: str,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__parentPath = parentPath
        self.__logger = logger
        self.__gateway = gateway if gateway is not None else []
        self.__localPersistence = True if 'local' in self.__gateway else False

        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)

        if not os.path.exists(f'{self.__parentPath}/logs'):
            os.makedirs(f'{self.__parentPath}/logs')
        pass

    def run(
        self,
        service: str,
        host: str,
        port: str,
        db: str,
        user: str,
        password: str,
        mechanism: str
    ) -> bool:
        try:
            now = datetime.now()
            dirName = now.strftime("%Y-%m-%d_%H:%M:%S")

            serviceLog = open(
                f'{self.__parentPath}/logs/{service}_{dirName}.log',
                'a'
            )
            self.__logger.info(f"[{service}] Dump START")
            serviceLog.write(f"[{service}] Dump START\n")

            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                os.makedirs(path)

            cmd = [
                f'mongodump',
                f'--host={host}',
                f'--port={port}',
                f'--authenticationDatabase={db}',
                f'--username={user}',
                f'--password="{password}"',
                f"--authenticationMechanism={mechanism}",
                '--forceTableScan',
                f'--out={path}/{dirName}'
            ]

            with open(
                f'{self.__parentPath}/logs/{service}_{dirName}.log',
                'a'
            ) as f:
                runProcess(cmd, stderr=f)

            self.__logger.info(
                f"[{service}] Dump {path}/{dirName} COMPLETE"
            )
            serviceLog.write(
                f"[{service}] Dump {path}/{dirName} COMPLETE\n"
            )

            self.compressorTarGz(service, path, dirName, serviceLog)
            serviceLog.close()

        except Exception as e:
            self.__logger.error(
                f"[{service}] Dump FAILURE {e}"
            )

    def compressorTarGz(self, service, dirPath, dirName, serviceLog):
        try:
            self.__logger.info(
                f"[{service}] Create archive {dirPath}/{dirName}.tgz START"
            )
            serviceLog.write(
                f"[{service}] Create archive {dirPath}/{dirName}.tgz START\n"
            )

            DEVNULL = open(os.devnull, 'wb')
            cmd = [
                'tar',
                '-czvf',
                f'{dirPath}/{dirName}.tgz',
                '-C',
                f'{dirPath}',
                f'{dirName}'
            ]

            runProcess(
                cmd,
                stdout=DEVNULL,
                stderr=STDOUT,
                universal_newlines=True
            )
            self.__logger.info(
                f"[{service}] Archive {dirPath}/{dirName}.tgz CREATED"
            )
            serviceLog.write(
                f"[{service}] Archive {dirPath}/{dirName}.tgz CREATED\n"
            )

            locations = []
            locations = locations + self.__callGateway(
                dirPath,
                dirName
            )

            self.__logger.debug(
                f"[{service}] Local persistance {self.__localPersistence}"
            )

            if self.__localPersistence is False:
                os.remove(f'{dirPath}/{dirName}.tgz')
                self.__logger.info(
                    f"[{service}] Local archive remove {dirPath}/{dirName}.tgz"
                )
            else:
                locations = locations + [
                    {
                        'location': 'frida',
                        'key': f'{dirPath}/{dirName}.tgz'
                    }
                ]

            self.__updateJsonStore(locations, dirPath, dirName)

        finally:
            DEVNULL.close()
            rmtree(f'{dirPath}/{dirName}')
            self.__logger.info(
                f"[{service}] {dirPath}/{dirName} DELETED"
            )
            serviceLog.write(f"[{service}] {dirPath}/{dirName} DELETED\n")

        self.__logger.info(
            f"[{service}] Archive {dirPath}/{dirName}.tgz COMPLETE"
        )

    def __callGateway(self, dirPath: str, fileName: str) -> list:
        locations = []
        for gatewayPath in self.__gateway:
            if gatewayPath != 'local':
                try:
                    g = Gateway.get(gatewayPath, self.__logger)
                    key = g.send(f'{dirPath}/{fileName}.tgz')
                    if key is None:
                        raise Exception("None key from gateway")
                    locations.append({'location': gatewayPath, 'key': key})
                except Exception as e:
                    self.__logger.error(f"Call gateway error {e}")
        return locations

    def __updateJsonStore(
        self,
        locations: list,
        dirPath: str,
        fileName: str
    ) -> None:
        jsonStore = {}
        if os.path.exists(f'{dirPath}/.jsonStore.json'):
            with open(f'{dirPath}/.jsonStore.json', 'r') as f:
                jsonStore = json.load(f)

        if len(locations) > 0:
            with open(f'{dirPath}/.jsonStore.json', 'w') as f:
                jsonItem = {
                    f"{fileName}": locations
                }
                jsonStore.update(jsonItem)
                json.dump(jsonStore, f)

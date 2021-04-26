import os
from subprocess import run as runProcess, STDOUT
from datetime import datetime
from logging import Logger
from shutil import rmtree
from src.gateway import Gateway


class MongoBk:
    def __init__(
        self,
        logger: Logger,
        dir: str,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        self.__gateway = gateway.split(',') if gateway is not None else []

        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)

        if not os.path.exists(f'{os.getenv("PARENT_PATH")}/logs'):
            os.makedirs(f'{os.getenv("PARENT_PATH")}/logs')
        pass

    def run(
        self,
        service: str,
        host: str,
        port: str,
        db: str,
        user: str,
        password: str
    ) -> bool:
        try:
            now = datetime.now()
            dirName = now.strftime("%Y-%m-%d_%H:%M:%S")

            serviceLog = open(
                f'{os.getenv("PARENT_PATH")}/logs/{service}_{dirName}.log',
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
                '--forceTableScan',
                f'--out={path}/{dirName}'
            ]
            with open(
                f'{os.getenv("PARENT_PATH")}/logs/{service}_{dirName}.log',
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
                f"[{service}] Create archive {dirPath}/{dirName}.tar.gz START"
            )
            serviceLog.write(
                f"[{service}] Create archive {dirPath}/{dirName}.tar.gz START\n"
            )

            DEVNULL = open(os.devnull, 'wb')
            cmd = [
                'tar',
                '-czvf',
                f'{dirPath}/{dirName}.tar.gz',
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
                f"[{service}] Archive {dirPath}/{dirName}.tar.gz CREATED"
            )
            serviceLog.write(
                f"[{service}] Archive {dirPath}/{dirName}.tar.gz CREATED\n"
            )
            # gateway
            for gatewayPath in self.__gateway:
                g = Gateway.get(gatewayPath)
                g.send(f'{dirPath}/{dirName}.tar.gz')

        finally:
            DEVNULL.close()
            rmtree(f'{dirPath}/{dirName}')
            self.__logger.info(
                f"[{service}] {dirPath}/{dirName} DELETED"
            )
            serviceLog.write(f"[{service}] {dirPath}/{dirName} DELETED\n")

        self.__logger.info(
            f"[{service}] Archive {dirPath}/{dirName}.tar.gz COMPLETE"
        )

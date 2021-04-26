from subprocess import run as runProcess, STDOUT
import os
from datetime import datetime
from src.gateway import Gateway


class MysqlBk:
    def __init__(
        self,
        logger,
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
            fileName = now.strftime("%Y-%m-%d_%H:%M:%S")

            serviceLog = open(
                f'{os.getenv("PARENT_PATH")}/logs/{service}_{fileName}.log',
                'a'
            )

            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                os.makedirs(path)

            self.__logger.info(f"[{service}] Dump START")
            serviceLog.write(f"[{service}] Dump START\n")

            cmd = [
                f'mysqldump',
                f'-h{host}',
                f'-P{port}',
                f'-u{user}',
                f'-p{password}',
                f'{db}'
            ]

            with open(
                f'{os.getenv("PARENT_PATH")}/logs/{service}_{fileName}.log',
                'a'
            ) as f:
                runProcess(
                    cmd,
                    stderr=f,
                    stdout=open(f'{path}/{fileName}.sql', 'w'),
                    universal_newlines=True
                )
            self.__logger.info(
                f"[{service}] Dump {path}/{fileName}.sql COMPLETE"
            )
            serviceLog.write(
                f"[{service}] Dump {path}/{fileName}.sql COMPLETE\n"
            )
            self.compressorTarGz(service, path, fileName, serviceLog)
            serviceLog.close()
        except Exception as e:
            self.__logger.error(
                f"[{service}] Dump FAILURE {e}"
            )

    def compressorTarGz(self, service, dirPath, fileName, serviceLog):
        try:
            self.__logger.info(
                f"[{service}] Create archive {dirPath}/{fileName}.tar.gz START"
            )
            serviceLog.write(
                f"[{service}] Create archive {dirPath}/{fileName}.tar.gz START\n"
            )
            DEVNULL = open(os.devnull, 'wb')
            cmd = [
                'tar',
                '-czvf',
                f'{dirPath}/{fileName}.tar.gz',
                '-C',
                f'{dirPath}',
                f'{fileName}.sql'
            ]
            runProcess(
                cmd,
                stdout=DEVNULL,
                stderr=STDOUT,
                universal_newlines=True
            )
            self.__logger.info(
                f"[{service}] Archive {dirPath}/{fileName}.tar.gz CREATED"
            )
            serviceLog.write(
                f"[{service}] Archive {dirPath}/{fileName}.tar.gz CREATED\n"
            )
            # gateway
            for gatewayPath in self.__gateway:
                g = Gateway.get(gatewayPath)
                g.send(f'{dirPath}/{fileName}.tar.gz')
        finally:
            DEVNULL.close()
            os.remove(f'{dirPath}/{fileName}.sql')
            self.__logger.info(
                f"[{service}] Archive {dirPath}/{fileName}.sql DELETED"
            )
            serviceLog.write(f"[{service}] {dirPath}/{fileName}.sql DELETED\n")
        self.__logger.info(
            f"[{service}] Archive {dirPath}/{fileName}.tar.gz COMPLETE"
        )

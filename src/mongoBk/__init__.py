import os
import subprocess
from datetime import datetime
from logging import Logger


class MongoBk:
    def __init__(
        self,
        logger: Logger,
        dir: str
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger

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
            dir_name = now.strftime("%Y-%m-%d_%H:%M:%S")

            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                os.makedirs(path)

            self.__logger.info(f"[{service}] Dump START")
            cmd = [
                f'mongodump',
                f'--host={host}',
                f'--port={port}',
                f'--authenticationDatabase={db}',
                f'--username={user}',
                f'--password="{password}"',
                f'--out={path}/{dir_name}'
            ]
            with open(
                f'{os.getenv("PARENT_PATH")}/logs/{service}_{dir_name}.log',
                'a'
            ) as f:
                subprocess.run(cmd, stderr=f, universal_newlines=True)
            self.__logger.info(f"[{service}] Dump FINISH -> {path}/{dir_name}")
        except Exception as e:
            self.__logger.error(
                f"[{service}] Dump FAILURE {e}"
            )

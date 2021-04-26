import os
import re
from datetime import datetime
from logging import Logger
from src.gateway import Gateway


class ClearMongoBk:
    def __init__(
        self,
        logger: Logger,
        dir: str,
        date: datetime,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        self.__date = date
        self.__gateway = gateway.split(',') if gateway is not None else []
        pass

    def run(
        self,
        service: str
    ) -> None:
        self.__deleteDirs(service)
        self.__deleteLogs(service)

    def __deleteDirs(self, service: str) -> None:
        try:
            count = 0
            path = f'{self.__dir_path}/{service}'

            if not os.path.exists(path):
                self.__logger.error(
                    f"[{service}] Mongo clear path {path} not found"
                )
                return None

            r = re.compile('^[\d]{4}-[\d]{2}-[\d]{2}_[\d]{2}:[\d]{2}:[\d]{2}\.tgz$')
            self.__logger.info(f"[{service}] Mongo clear")
            for archiveName in list(filter(r.match, os.listdir(path))):
                if datetime.strptime(archiveName[:-4].replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__date:
                    try:
                        os.remove(f'{path}/{archiveName}')
                        self.__logger.info(
                            f"[{service}] Mongo clear archive deleted -> {path}/{archiveName}"
                        )
                        # gateway
                        for gatewayPath in self.__gateway:
                            g = Gateway.get(gatewayPath)
                            g.delete(f'{path}/{archiveName}')
                        count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[{service}] Mongo archive delete -> {path}/{archiveName} error: {e}"
                        )
            self.__logger.info(
                f"[{service}] Mongo clear FINISH {count} archive deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo clear FAILURE {e}"
            )

    def __deleteLogs(self, service: str) -> None:
        try:
            count = 0
            path = f'{os.getenv("PARENT_PATH")}/logs'
            r = re.compile(f'^{service}_[\d]{{4}}-[\d]{{2}}-[\d]{{2}}_[\d]{{2}}:[\d]{{2}}:[\d]{{2}}\.log$')
            self.__logger.info(f"[{service}] Mongo log files clear START")
            for filename in list(filter(r.match, os.listdir(path))):
                file_noservice = filename.replace(f"{service}_", "")
                if datetime.strptime(file_noservice[:-4].replace("_", " "), "%Y-%m-%d %H:%M:%S") < self.__date:
                    try:
                        os.remove(f"{path}/{filename}")
                        self.__logger.info(
                            f"[{service}] delete -> {path}/{filename}"
                        )
                        count = count + 1
                    except Exception as e:
                        self.__logger.error(
                            f"[{service}] Mongo logs file delete -> {path}/{filename} error: {e}"
                        )
            self.__logger.info(
                f"[{service}] Mongo logs clear FINISH {count} files deleted"
            )
        except Exception as e:
            self.__logger.error(
                f"[{service}] Mongo logs clear  error: {e}"
            )

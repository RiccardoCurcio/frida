from subprocess import run as runProcess, STDOUT
import os
import json
from datetime import datetime
from src.gateway import Gateway


class Mysql:
    def __init__(
        self,
        logger,
        dir: str,
        gateway: str = None
    ) -> None:
        self.__dir_path = dir
        self.__logger = logger
        self.__gateway = gateway.split(',') if gateway is not None else []
        self.__localPersistence = True if 'local' in self.__gateway else False

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
                f"[{service}] Create archive {dirPath}/{fileName}.tgz START"
            )
            serviceLog.write(
                f"[{service}] Create archive {dirPath}/{fileName}.tgz START\n"
            )
            DEVNULL = open(os.devnull, 'wb')
            cmd = [
                'tar',
                '-czvf',
                f'{dirPath}/{fileName}.tgz',
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
                f"[{service}] Archive {dirPath}/{fileName}.tgz CREATED"
            )
            serviceLog.write(
                f"[{service}] Archive {dirPath}/{fileName}.tgz CREATED\n"
            )
            
            locations = []
            locations = locations + self.__callGateway(
                dirPath,
                fileName
            )
            
            self.__logger.debug(f"[{service}] Local persistance {self.__localPersistence}")
            
            if self.__localPersistence is False:
                os.remove(f'{dirPath}/{fileName}.tgz')
                self.__logger.info(f"[{service}] Local archive remove {dirPath}/{fileName}.tgz")
            else:
                 locations = locations + [{'location': 'frida', 'key': f'{dirPath}/{fileName}.tgz'}]
            
            self.__updateJsonStore(locations, dirPath, fileName)
        finally:
            DEVNULL.close()
            os.remove(f'{dirPath}/{fileName}.sql')
            self.__logger.info(
                f"[{service}] Archive {dirPath}/{fileName}.sql DELETED"
            )
            serviceLog.write(f"[{service}] {dirPath}/{fileName}.sql DELETED\n")
        self.__logger.info(
            f"[{service}] Archive {dirPath}/{fileName}.tgz COMPLETE"
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

    def __updateJsonStore(self, locations: list, dirPath: str, fileName: str) -> None:
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

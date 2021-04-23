import subprocess
import os
from datetime import datetime

class MysqlBk:
    def __init__(self, logger, dir:str) -> None:
        self.__dir_path = dir
        self.__logger = logger
        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)
            
        if not os.path.exists(f'{os.getenv("PARENT_PATH")}/logs'):
            os.makedirs(f'{os.getenv("PARENT_PATH")}/logs')
        pass
    
    def run(self, service:str, host:str, port:str, db:str, user:str, password:str) -> bool:
        
        now = datetime.now()
        file_name = now.strftime("%Y-%m-%d_%H:%M:%S")
        
        path = f'{self.__dir_path}/{service}'
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        self.__logger.info(f"[{service}] Dump START")
        cmd = [
            f'mysqldump',
            f'-h{host}',
            f'-P{port}',
            f'-u{user}',
            f'-p{password}',
            f'{db}'
        ]
        with open(f'{os.getenv("PARENT_PATH")}/logs/{service}_{file_name}.log', 'a') as f:
            subprocess.run(cmd, stderr=f, stdout=open(f'{path}/{file_name}.sql', 'w'), universal_newlines=True)
        self.__logger.info(f"[{service}] Dump FINISH -> {path}/{file_name}.sql")
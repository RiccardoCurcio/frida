import os
import subprocess
from datetime import datetime

class MongoBk:
    def __init__(self, dir:str) -> None:
        self.__dir_path = dir
        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)
        
        if not os.path.exists(f'{os.getenv("PARENT_PATH")}/logs'):
            os.makedirs(f'{os.getenv("PARENT_PATH")}/logs')
        pass
    
    def run(self, service:str, host:str, port:str, db:str, user:str, password:str) -> bool:
        
        now = datetime.now()
        dir_name = now.strftime("%Y-%m-%d_%H:%M:%S")
        
        path = f'{self.__dir_path}/{service}'
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        print(f"[{service}] Dump \033[92mSTART\033[0m")
        cmd = [
            f'mongodump',
            f'--host={host}',
            f'--port={port}',
            f'--authenticationDatabase={db}',
            f'--username={user}',
            f'--password="{password}"',
            f'--out={path}/{dir_name}'
        ]   

        with open(f'{os.getenv("PARENT_PATH")}/logs/{service}_{dir_name}.log', 'a') as f:
            subprocess.run(cmd, stderr=f, universal_newlines=True)
        
        print(f"[{service}] Dump \033[92mFINISH\033[0m -> {path}/{dir_name}")
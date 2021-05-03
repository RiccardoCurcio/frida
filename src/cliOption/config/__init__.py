import re
import configparser
import os
import sys


class Config:

    @staticmethod
    def setConfig(args) -> configparser.ConfigParser:
        try:
            configFile = 'config.ini'
            config = configparser.ConfigParser()

            r = re.compile('^--config=.*\\.ini')
            confParam = list(filter(r.match, args))

            if len(confParam) == 1:
                configFile = Config.checkConfigFile(confParam[0][9:])
            else:
                configFile = Config.checkConfigFile(configFile)
            os.environ["CONFIG_FILE"] = configFile
            config.read(f'{configFile}')
            return config
        except Exception as e:
            print(f"configparser ini error {e}")
            sys.exit(1)

    @staticmethod
    def checkConfigFile(configFile: str) -> bool:
        try:
            if os.path.isfile(f'{os.getenv("FRIDA_PARENT_PATH")}/{configFile}'):
                return f'{os.getenv("FRIDA_PARENT_PATH")}/{configFile}'
            elif os.path.isfile(f'{configFile}'):
                return f'{configFile}'
            else:
                print("Not valid Config file")
                sys.exit(1)
        except Exception as e:
            print(f"Not valid Config file {e}")
            sys.exit(1)

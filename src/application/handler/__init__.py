import sys
import logging
import re
from configparser import ConfigParser
from src.dependencies import Dependencies
from src.application.handler.handler.backup import Backup
from src.application.handler.handler.clear import Clear
from src.application.handler.handler.list import List
from src.application.handler.handler.help import Help
from src.application.handler.handler.check import Check
from src.application.handler.handler.version import Version


class HandlerFactory:

    @staticmethod
    def run(config: ConfigParser, logger: logging.Logger, args: list) -> None:
        """[Run]

        Args:
            config (ConfigParser): [config parser]
            logger (logging.Logger): [logger]
            args (list): [arg list]
        """
        if "--list" in args or "-l" in args:
            HandlerFactory.allowedFlag("list", args)
            # call list handeler
            handler = List(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--check" in args or "-C" in args:
            HandlerFactory.allowedFlag("check", args)
            # call check handeler
            Dependencies(logger).check()
            handler = Check(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--help" in args or "-h" in args:
            HandlerFactory.allowedFlag("help", args)
            # call help handeler
            handler = Help(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--version" in args or "-v" in args:
            HandlerFactory.allowedFlag("version", args)
            # call version handeler
            handler = Version(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--backup" in args or "-b" in args:
            HandlerFactory.allowedFlag("backup", args)
            Dependencies(logger).check()
            # call backup handeler
            handler = Backup(config, logger, args)
            handler.run()
            # if "--clear" in args or "-c" in args:
            #     # call clear handeler
            #     handler = Clear(config, logger, args)
            #     handler.run()
            sys.exit(0)
        elif "--clear" in args or "-c" in args:
            HandlerFactory.allowedFlag("clear", args)
            Dependencies(logger).check()
            # call clear handeler
            handler = Clear(config, logger, args)
            handler.run()
            sys.exit(0)
        else:
            # help
            handler = Help(config, logger, args)
            handler.run()
            sys.exit(1)

    @staticmethod
    def allowedFlag(cmd: str, args: list):
        checkArgs = args[1:]
        allowed = {
            "check": {
                "options": ["-C", "--check", "--config", "--service"]
            },
            "clear": {
                "options": ["-c", "--clear", "--config", "--service", "--clear-interval", "--gateway", "--clear-gateway-except"]
            },
            "backup": {
                "options": ["-b", "--backup", "--config", "--service", "--gateway"]
            },
            "list": {
                "options": ["-l", "--list", "--config", "--service"]
            },
            "help": {
                "options": ["-h", "--help"]
            },
            "version": {
                "options": ["-v", "--version"]
            }
        }
        for cli in checkArgs:
            opt = cli.split('=')[0]
            r = re.compile(f'^{opt}.*$')
            confParam = list(filter(r.match, allowed[cmd]["options"]))
            if len(confParam) == 0:
                print(f'{opt} Not valid option show help')
                sys.exit(1)

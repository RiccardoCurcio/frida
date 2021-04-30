"""[summary]
"""
import sys
import logging
from configparser import ConfigParser
from src.dependencies import Dependencies
from src.application.handler.handler.backup import Backup
from src.application.handler.handler.clear import Clear
from src.application.handler.handler.list import List
from src.application.handler.handler.help import Help
from src.application.handler.handler.version import Version


class HandlerFactory:

    @staticmethod
    def run(config: ConfigParser, logger: logging.Logger, args: list) -> None:
        if "--list" in args or "-l" in args:
            # call list handeler
            handler = List(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--backup" in args or "-b" in args:
            Dependencies(logger).check()
            # call backup handeler
            handler = Backup(config, logger, args)
            handler.run()
            if "--clear" in args or "-c" in args:
                # call clear handeler
                handler = Clear(config, logger, args)
                handler.run()
            sys.exit(0)
        elif "--clear" in args or "-c" in args:
            Dependencies(logger).check()
            # call clear handeler
            handler = Clear(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--help" in args or "-h" in args:
            # call help handeler
            handler = Help(config, logger, args)
            handler.run()
            sys.exit(0)
        elif "--version" in args or "-v" in args:
            # call version handeler
            handler = Version(config, logger, args)
            handler.run()
            sys.exit(0)
        else:
            # help
            handler = Help(config, logger, args)
            handler.run()
            sys.exit(1)

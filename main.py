import sys
import os
import pathlib
from src.bootstrap import Bootstrap
from src.backup import Backups
from src.database import DbConnection
import configparser



if __name__ == '__main__':
    try:
        if "--help" in sys.argv or "-h" in sys.argv:
            print("help")
            sys.exit(0)
        if "--version" in sys.argv or "-v" in sys.argv:
            print("0.0")
            sys.exit(0)
        if "--config" in sys.argv:
            print("get config file")

        os.environ["PARENT_PATH"] = f'{pathlib.Path(__file__).parent}'

        config = configparser.ConfigParser()
        config.read(f'{os.getenv("PARENT_PATH")}/config.ini')

        boot = Bootstrap(config)
        logger = boot.setLogger()

        dbs = DbConnection(logger)
        
        if "--backup" in sys.argv or "-b" in sys.argv:
            if "--only" in sys.argv or "-o" in sys.argv:
                print("only name")
            bk = Backups(logger)
            bk.run(dbs, config)
        if "--clear" in sys.argv or "-c" in sys.argv:
            if "--only" in sys.argv or "-o" in sys.argv:
                print("only name")
            print("clear")
        
       
        
    except KeyboardInterrupt:
        logger.info('Stopping script...')
        sys.exit(0)
    except Exception as e:
        logger.error(f'There was an error while starting process: {e}')
        sys.exit(1)

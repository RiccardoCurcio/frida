import sys
import os
import pathlib
from src.bootstrap import Bootstrap
from src.backup import Backups
from src.database import DbConnection
import configparser



if __name__ == '__main__':
    try:
        # sudo apt-get install mysql-client
        # crontab
        # @midnight
        # */5 * * * * python3 /home/riccardo/Develop/coloombus/dbs_backups/main.py
        
        # arg --config get specific ini file
        # arg --config-gen create new ini file
        # arg --clear or -c clear old backup
        # arg --backup or -b create backup
        # arg --only or -o name service
        # arg --help or -h create backup
        # arg --version or -v vesion
        
        # gzip
        # scp
        
        os.environ["PARENT_PATH"] = f'{pathlib.Path(__file__).parent}'

        config = configparser.ConfigParser()
        config.read(f'{os.getenv("PARENT_PATH")}/config.ini')

        boot = Bootstrap(config)
        logger = boot.setLogger()
        
        dbs = DbConnection(logger)
        bk = Backups()
        bk.run(dbs, config)
        
    except KeyboardInterrupt:
        logger.info('Stopping script...')
        sys.exit(0)
    except Exception as e:
        logger.error(f'There was an error while starting process: {e}')
        sys.exit(1)

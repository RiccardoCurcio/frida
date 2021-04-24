# backup
python3 backup
python3 main.py --config=config.ini -b --only=api_import

# todo      

arg --help or -h print help [todo]
arg --version or -v vesion [todo]
arg --list or -l -> --only=api_import [todo]
gzip [todo]
scp [todo]

arg --clear or -c clear old backup [done]
arg --config get specific ini file [done]
arg --backup or -b create backup [done]
arg --only or -o name service [done]

# sudo apt-get install mysql-client
# crontab
# @midnight
# */5 * * * * python3 /home/riccardo/Develop/coloombus/dbs_backups/main.py


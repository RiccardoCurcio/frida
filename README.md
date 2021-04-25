# backup
python3 -m backup -b

python3 -m backup --config=config.ini -b --only=api_import

python3 -m backup --config=config.ini -l --only=mongo_dbs

python3 -m backup --config=config.ini -c --only=mongo_dbs

# todo
create a cronjob [todo]
scp [todo]

check dependencies mysqldump, mongodump, git [done]
arg --clear or -c clear old backup [done]
arg --config get specific ini file [done]
arg --backup or -b create backup [done]
arg --only name service [done]
arg --list or -l -> --only=api_import [done]
arg --help or -h print help [done]
arg --version or -v vesion [done]
tar.gz [done]

# sudo apt-get install mysql-client
# crontab
# @midnight
# */5 * * * * python3 -m backup -b


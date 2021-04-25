# Frida

Create backup from multiple database mongoDB, mysql, mariaDB

# Installation

```
    $ git clone -b <tag or branch> https://github.com/RiccardoCurcio/backup

    $ pip3 install -r requirements.txt

    $ python3 -m frida -h
```

# Config.ini example

Frida need a config file

```ini
[DEFAULT]
# default level INFO
LOGGING_LEVEL = DEBUG
# days (default 365)
CLEAR = 365
# dir default ./backups
# DIR = /custom/path/of/folder/backup

[mysql_service_name_1]
TYPE = mysql
DB_HOST = 127.0.0.1
DB_PORT = 3306
DB_DATABASE = dbname
DB_USERNAME = username
DB_PASSWORD = password
# default from DEFAULT
# DIR = /mysql_service_name_1/custom/path/of/folder/backup

[mysql_service_name_2]
TYPE = mysql
DB_HOST = 127.0.0.1
DB_PORT = 3307
DB_DATABASE = dbname
DB_USERNAME = username
DB_PASSWORD = password
# default from DEFAULT
# DIR = /mysql_service_name_2/custom/path/of/folder/backup

[mongo_service_name_1]
TYPE = mongo
DB_HOST = localhost
DB_PORT = 27017
DB_DATABASE = auth-db-name
DB_USERNAME = username
DB_PASSWORD = password
DB_MECHANISM = SCRAM-SHA-256
# default from DEFAULT
# DIR = /mongo_service_name_1/custom/path/of/folder/backup

[mongo_service_name_2]
TYPE = mongo
DB_HOST = localhost
DB_PORT = 27018
DB_DATABASE = auth-db-name
DB_USERNAME = username
DB_PASSWORD = password
DB_MECHANISM = SCRAM-SHA-256
# default from DEFAULT
# DIR = /mongo_service_name_2/custom/path/of/folder/backup

```
# Usage
```
    // create backup archive for all services
    $ python3 -m frida -b

    // create backup archive for all services use different config file
    $ python3 -m frida --config=custom_config.ini

    // create backup archive only for services mysql_service_name_2 and mongo_service_name_1
    $ python3 -m frida --config=custom_config.ini -b --only=mysql_service_name_2,mongo_service_name_1

    // list of backups use different config file
    $ python3 -m frida --config=custom_config.ini -l
    
    // list of backups
    $ python3 -m frida -l

    // clear all old backup
    $ python3 -m frida -c

    // create backup and clear old backup
    $ python3 -m frida -b -c

    // clear all old backup for service mysql_service_name_2
    $ python3 -m frida -c --only=mysql_service_name_2

    // Print help
    $ python3 -m frida -h
```

# Create a cronjob with crontab
```
    @midnight python3 -m frida -b
```
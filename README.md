# Frida

Create backup (tgz archive) from multiple database mongoDB, mysql, mariaDB

# Installation

```
    $ git clone -b <tag or branch> https://github.com/RiccardoCurcio/frida

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
CLEAR_INTERVAL = 365
# dir default ./backups
# DIR = /custom/path/of/folder/backup

[mysql_service_name_1]
TYPE = mysql
DB_HOST = 127.0.0.1
DB_PORT = 3306
DB_DATABASE = dbname
DB_USERNAME = username
DB_PASSWORD = password
# send archive to external storage
; if GATEWAY is set and 'local' is in list of gateway the local the archives will be persistent
; GATEWAY = custom.customgateway,s3,local
# clear from external storage
; CLEAR_GATEWAY_EXCEPT = custom.customgateway
# custom clear value 
; CLEAR_INTERVAL = 2
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
    $ python3 -m frida --config=custom_config.ini -b

    // create backup archive only for services mysql_service_name_2 and mongo_service_name_1
    $ python3 -m frida --config=custom_config.ini -b --service=mysql_service_name_2,mongo_service_name_1

    // create backup archive for service mysql_service_name_2 and override gateway value
    $ python3 -m frida -b --service=mysql_service_name_2 --gateway=local

    // list of backups use different config file
    $ python3 -m frida --config=custom_config.ini -l
    
    // list of backups
    $ python3 -m frida -l

    // clear all old backup
    $ python3 -m frida -c

    // create backup and clear old backup
    $ python3 -m frida -b -c

    // clear all old backup for service mysql_service_name_2
    $ python3 -m frida -c --service=mysql_service_name_2

    // clear all old backup for all services with ovveride clear interval value
    python3 -m frida --config=config.ini -c --clear-interval=NOW

    // clear all old backup for all services with ovveride clear interval value
    python3 -m frida --config=config.ini -c --clear-interval=10

    // clear all old backup for service mysql_service_name_2 override gateway value override clear gateway except value
    python3 -m frida -c --service=mysql_service_name_2  --gateway=local --clear-gateway-except

    // clear all old backup for service mysql_service_name_2 override gateway value and override clear gateway except value
    python3 -m frida -c --service=mysql_service_name_2  --gateway=local --clear-gateway-except=custom.customgateway

    // clear all old backup for service mysql_service_name_2 override clear gateway except value (empty the exceptions)
    python3 -m frida -c --service=mysql_service_name_2 --clear-gateway-except 

    // Print help
    $ python3 -m frida -h
```
# Create Custom gateway
```
    // create new directory in gateways/custom
    $ cd gateways/custom && mkdir custom_gateway

    // create file __init__.py
    $ cd custom_gateway && touch __init__.py
```

Copy this code

```python
from gateways.GatewayABC import GatewayABC
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv, find_dotenv


class CustomGateway(GatewayABC):
    def __init__(self, logger):
        self.__logger = logger

    def send(self, archivePath) -> str:
        key = "custom_key"
        try:
            self.__logger.info(f"Custom gateway send")
        except Exception as e:
            self.__logger.error(f"Custom gateway send error {e}")
        return key

    def delete(self, key):
        key = "custom_key"
        try:
            self.__logger.info(f"Custom gateway delete")
        except Exception as e:
            self.__logger.error(f"Custom gateway delete error {e}")
        pass

```

if your custom gateway has new requirements.txt file

```
    $ pip3 install -r gateways/custom/custom_gateway/requirements.txt
``` 

Enable gateway in service session

```ini
[mysql_service_name_1]
TYPE = mysql
DB_HOST = 127.0.0.1
DB_PORT = 3306
DB_DATABASE = dbname
DB_USERNAME = username
DB_PASSWORD = password
# send archive to external storage
GATEWAY = custom.custom_gateway,s3
# custom clear value 
CLEAR_INTERVAL = 2
# default from DEFAULT
# DIR = /mysql_service_name_1/custom/path/of/folder/backup
```


# Create a cronjob with crontab [example]
```
    @midnight python3 -m /path/of/frida -b
```

    If you're wondering, Frida is my dog's name
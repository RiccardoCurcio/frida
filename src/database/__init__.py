from pymongo.mongo_client import MongoClient
import pymysql


class DbConnection:

    def __init__(self, logger):
        self.__logger = logger
        pass

    def mongoconnect(self, host, port, db, user, password, mechanism='SCRAM-SHA-256') -> bool:
        try:
            client = MongoClient(host+':'+port)
            client[db].authenticate(
                user,
                password,
                mechanism=mechanism
            )
        except Exception as e:
            self.__logger.error(f"Error: {e}")
            return False
        client.close()
        return True

    def mysqlconnect(self, host, port, db, user, password, charset='utf8') -> bool:
        try:
            connection = pymysql.connect(
                host=host,
                port=int(port),
                db=db,
                user=user,
                password=password,
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            self.__logger.error(f'Error: {e}')
            return False
        connection.close()
        return True

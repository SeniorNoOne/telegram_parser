from pymongo.mongo_client import MongoClient

from utils.common import logger


class DB:
    def __init__(self, uri, user_table_name, msg_table_name):
        self._db_client = MongoClient(uri)
        self.user_table_name = user_table_name
        self.msg_table_name = msg_table_name
        self.user_table = self._db_client[user_table_name]
        self.msg_table = self._db_client[msg_table_name]

        self.ping()

    def ping(self):
        try:
            self._db_client.admin.command('ping')
            logger.info('Connection to DB is established')
        except Exception as e:
            print(e)

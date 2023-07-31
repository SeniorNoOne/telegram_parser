from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError

from utils.common import logger, log_func_call


class DB:
    def __init__(self, event_manager, uri, db_name, user_table_name, msg_table_name):
        self.event_manager = event_manager

        self.db_name = db_name
        self.user_table_name = user_table_name
        self.msg_table_name = msg_table_name

        self._db_client = MongoClient(uri)
        self._db = self._db_client[db_name]
        self.user_table = self._db[user_table_name]
        self.msg_table = self._db[msg_table_name]

        self.user_table.create_index('id', unique=True)

        self.ping()

    @log_func_call
    def ping(self):
        try:
            self._db_client.admin.command('ping')
            logger.info('Connection to DB is established')
        except Exception as e:
            logger.info(e)

    @log_func_call
    def insert_user(self, data):
        try:
            self.user_table.insert_one(data)
        except DuplicateKeyError:
            logger.info('Duplicate user document. Skipping')

    @log_func_call
    def insert_msg(self, data):
        try:
            self.msg_table.insert_one(data)
        except DuplicateKeyError:
            logger.info('Duplicate message document. Skipping')

    @log_func_call
    def update_user(self, data):
        self.user_table.update_one({'id': data['id']}, {'$set': data})

    @log_func_call
    def update_msg(self, update, data):
        self.msg_table.update_one(update, {'$set': data})

    @log_func_call
    def fetch_users(self, user_filter=()):
        users = self.user_table.find(user_filter)
        users = list(users)
        return users

    @log_func_call
    def fetch_target_words(self, user_filter=()):
        users = self.fetch_users(user_filter=user_filter)

        target_words = []
        for user in users:
            target_words.extend(user['target_words'])
        return target_words

from pymongo.mongo_client import MongoClient
from pymongo.errors import DuplicateKeyError

from utils.common import logger, log_func


class DB:
    def __init__(self, event_manager, uri, db_name, user_table_name, parsed_data_table_name):
        self.event_manager = event_manager

        # DB config
        self.db_name = db_name
        self.user_table_name = user_table_name
        self.parsed_data_table_name = parsed_data_table_name

        # DB connection instances
        self._db_client = MongoClient(uri)
        self._db = self._db_client[db_name]
        self.user_table = self._db[user_table_name]
        self.parsed_data_table = self._db[parsed_data_table_name]

        # DB indexes
        self.user_table.create_index('id', unique=True)
        self.parsed_data_table.create_index('post_link', unique=True)
        self.ping()

    @log_func
    def ping(self):
        try:
            self._db_client.admin.command('ping')
            logger.info('Connection to DB is established')
        except Exception as e:
            logger.info(e)

    @log_func
    def insert_user(self, user_data):
        try:
            self.user_table.insert_one(user_data)
        except DuplicateKeyError:
            logger.info('Duplicate user document. Skipping')

    @log_func
    def insert_parsed_data(self, parsed_data):
        try:
            self.parsed_data_table.insert_one(parsed_data)
        except DuplicateKeyError:
            logger.info('Duplicate parsed data document. Skipping')

    @log_func
    def update_user(self, data):
        self.user_table.update_one({'id': data['id']}, {'$set': data})

    @log_func
    def update_parsed_data(self, data):
        self.parsed_data_table.update_one({'post_link': data['post_link']}, {'$set': data})

    @log_func
    def fetch_user(self, user_id):
        user = self.user_table.find_one({'id': user_id})
        return user

    @log_func
    def fetch_users(self):
        user = self.user_table.find()
        return list(user)

    @log_func
    def fetch_target_words(self, user_id):
        user = self.fetch_user(user_id)
        return user['target_words']

    @log_func
    def fetch_parsed_data(self, post_link):
        parsed_data = self.parsed_data_table.find_one({'post_link': post_link})
        return parsed_data

    @log_func
    def fetch_parsed_data_by_user_id(self, user_id):
        parsed_data = list(self.parsed_data_table.find())
        parsed_data = [post for post in parsed_data if user_id in post['user_id']]
        return parsed_data

    @log_func
    def delete_user(self, user_id):
        self.user_table.delete_one({'id': user_id})

    @log_func
    def delete_parsed_data(self, user_id):
        posts = list(self.parsed_data_table.find())

        for post in posts:
            if user_id in post['user_id']:
                if len(post['user_id']) > 1:
                    post['user_id'].remove(user_id)
                    self.parsed_data_table.update_many({'post_link': post['post_link']},
                                                       {'$set': post})
                else:
                    self.parsed_data_table.delete_one({'post_link': post['post_link']})

import mysql.connector
import configparser
import json

config = configparser.ConfigParser()
config.read("config/config.ini")


host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']


class DB:
    def __init__(self, event_manager, host, user, password, database):
        self.event_manager = event_manager

        # DB config
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        # DB connection instances
        self._db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self._cursor = self._db.cursor()

        self.create_user_table = "CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, `data` JSON NOT NULL);"
        self.create_parsed_data_table = "CREATE TABLE parsed_data (id INT AUTO_INCREMENT PRIMARY KEY, `data` JSON NOT NULL);"

        self.user_insert_sql = "INSERT INTO user (data) VALUES (%s)"
        self.parsed_data_insert_sql = "INSERT INTO parsed_data (data) VALUES (%s)"

        self.user_update_sql = "UPDATE user SET data = %s WHERE JSON_EXTRACT(data, %s) = %s"
        self.parsed_data_update_sql = "UPDATE parsed_data SET data = %s WHERE id = %s"
        # self._cursor.execute(self.create_user_table)
        # self._cursor.execute(self.create_parsed_data_table)

    @staticmethod
    def to_json(data):
        return json.dumps(data)

    def insert_user(self, user_data):
        user_data = self.to_json(user_data)
        self._cursor.execute(self.user_insert_sql, (user_data,))
        self._db.commit()

    def insert_parsed_data(self, parsed_data):
        parsed_data = self.to_json(parsed_data)
        self._cursor.execute(self.parsed_data_insert_sql, (parsed_data,))
        self._db.commit()

    def update_user(self, data):
        val = (self.to_json(data), f'$.id', self.to_json(data))
        self._cursor.execute(self.user_update_sql, val)
        self._db.commit()

    def update_parsed_data(self, data):
        val = (self.to_json(data), f'$.id', self.to_json(data))
        self._cursor.execute(self.user_update_sql, val)
        self._db.commit()


db = DB(None, host, user, password, database)
db.insert_user({'id': 1, 'name': 'user'})
db.insert_parsed_data({'id': 11525, 'name': 'user'})
db.update_user({'id': 1, 'name': 'Snutras'})

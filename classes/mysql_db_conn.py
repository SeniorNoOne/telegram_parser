import mysql.connector
import configparser
import json


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
            database=self.database,
            autocommit=True
        )
        self._cursor = self._db.cursor()

        # SQL queries
        self.create_user_table = (
            "CREATE TABLE IF NOT EXISTS user ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "data JSON NOT NULL)"
        )
        self.create_parsed_data_table = (
            "CREATE TABLE IF NOT EXISTS parsed_data ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "data JSON NOT NULL)"
        )

        # Insert
        self.user_insert_sql = "INSERT INTO user (data) VALUES (%s)"
        self.parsed_data_insert_sql = "INSERT INTO parsed_data (data) VALUES (%s)"

        # Update
        self.user_update_sql = ("UPDATE user SET data = %s "
                                "WHERE JSON_EXTRACT(data, '$.id') = %s")
        self.parsed_data_update_sql = ("UPDATE parsed_data SET data = %s "
                                       "WHERE JSON_EXTRACT(data, '$.post_link') = %s")

        # Fetch
        self.user_fetch_sql = "SELECT * FROM user WHERE id = {}"
        self.users_fetch_sql = "SELECT * FROM user"
        self.parsed_data_fetch_sql_ = "SELECT * FROM parsed_data"
        self.parsed_data_fetch_sql = ("SELECT * FROM parsed_data "
                                      "WHERE JSON_UNQUOTE(JSON_EXTRACT("
                                      "data, '$.post_link')) = '{}'")

        # Delete
        self.user_delete_sql = ("DELETE FROM user "
                                "WHERE JSON_UNQUOTE(JSON_EXTRACT(data, '$.id')) = '{}'")
        self.parsed_data_delete_sql = ("DELETE FROM parsed_data "
                                       "WHERE JSON_UNQUOTE(JSON_EXTRACT("
                                       "data, '$.post_link')) = '{}'")

        # Creating required tables
        self._cursor.execute(self.create_user_table)
        self._cursor.execute(self.create_parsed_data_table)

    @staticmethod
    def to_json(data):
        return json.dumps(data)

    def insert_user(self, user_data):
        user_data = self.to_json(user_data)
        self._cursor.execute(self.user_insert_sql, (user_data,))

    def insert_parsed_data(self, parsed_data):
        parsed_data = self.to_json(parsed_data)
        self._cursor.execute(self.parsed_data_insert_sql, (parsed_data,))

    def update_user(self, data):
        val = (self.to_json(data), data['id'])
        self._cursor.execute(self.user_update_sql, val)

    def update_parsed_data(self, data):
        val = (self.to_json(data), data['post_link'])
        self._cursor.execute(self.parsed_data_update_sql, val)

    def fetch_user(self, user_id):
        sql = self.user_fetch_sql.format(user_id)
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetch_users(self):
        self._cursor.execute(self.users_fetch_sql)
        return self._cursor.fetchall()

    def fetch_parsed_data(self, post_link):
        sql = self.parsed_data_fetch_sql.format(post_link)
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def fetch_parsed_data_by_user_id(self, user_id):
        self._cursor.execute(self.parsed_data_fetch_sql_)
        parsed_data = self._cursor.fetchall()
        res = []

        for item in parsed_data:
            js = json.loads(item[1])
            if user_id in js.get('user_id', []):
                res.append(js)

        return res

    def delete_user(self, user_id):
        sql = self.user_delete_sql.format(user_id)
        self._cursor.execute(sql)

    def delete_parsed_data(self, user_id):
        self._cursor.execute(self.parsed_data_fetch_sql_)
        posts = self._cursor.fetchall()

        for post in posts:
            id_, js = post
            js = json.loads(js)

            if user_id in js.get('user_id', []):
                if len(js.get('user_id', [])) > 1:
                    js['user_id'].remove(user_id)
                    self.update_parsed_data(js)
                else:
                    sql = self.parsed_data_delete_sql.format(js['post_link'])
                    self._cursor.execute(sql)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("../config/config.ini")

    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']
    database = config['mysql']['database']

    db = DB(None, host, user, password, database)
    db.insert_user({'id': 100, 'name': 'user'})
    db.insert_parsed_data({'post_link': 10, 'user_id': [5, 6], 'message': 'Snutra kebab'})
    db.update_user({'id': 1, 'name': 'Snutras'})
    db.fetch_user(4)
    db.fetch_users()
    db.fetch_parsed_data(10)
    db.fetch_parsed_data_by_user_id(3)
    db.delete_user(2)
    db.delete_parsed_data(6)

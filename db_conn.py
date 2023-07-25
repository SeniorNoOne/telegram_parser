import configparser

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Reading Configs
config = configparser.ConfigParser()
config.read("config/config.ini")

# Setting configuration values
uri = config['DB']['uri']

# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    db_client.admin.command('ping')
    print('Connected to MongoDB')

    db = db_client['parsed_msg']
except Exception as e:
    print(e)

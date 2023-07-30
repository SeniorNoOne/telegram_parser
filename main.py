import asyncio
import configparser

from classes.bot import CustomBot
from classes.db_conn import DB
from classes.parser import Parser
from utils.config import ui_config, db


if __name__ == '__main__':
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    username = config['Telegram']['username']
    bot_token = config['Telegram']['bot_token']

    # DB
    user_table_name = db['user_table_name']
    msg_table_name = db['msg_table_name']

    target_channel = 'https://t.me/test_parse_bot_1'
    target_words = ['.']

    db_uri = config['DB']['uri']

    bot = CustomBot(bot_token, ui_config)
    db = DB(db_uri, user_table_name, msg_table_name)
    parser = Parser(username, api_id, api_hash, target_channel, target_words)

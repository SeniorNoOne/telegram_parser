import asyncio
import configparser

from classes.bot import CustomBot
from classes.db_conn import DB
from classes.parser import Parser
from classes.dispatcher import Dispatcher
from classes.event_manager import EventManager
from utils.config import ui_config, db_config


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
    db_uri = config['DB']['uri']
    db_name = db_config['db_name']
    user_table_name = db_config['user_table_name']
    parsed_data_table_name = db_config['parsed_data_table_name']

    target_channel = 'https://t.me/test_parse_bot_1'
    target_words = []

    event_manager = EventManager()
    bot = CustomBot(event_manager, bot_token, ui_config)
    db = DB(event_manager, db_uri, db_name, user_table_name, parsed_data_table_name)
    parser = Parser(event_manager, username, api_id, api_hash, target_channel, target_words)

    dispatcher = Dispatcher(event_manager, bot, db, parser)
    asyncio.run(dispatcher.start())

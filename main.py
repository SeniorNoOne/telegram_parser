import asyncio
import configparser

from classes.bot import CustomBot
from classes.mongo_db_conn import DB
from classes.parser import Parser
from classes.dispatcher import Dispatcher
from classes.event_manager import EventManager
from utils.config import ui_config, db_config


if __name__ == '__main__':
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Parser
    api_id = config['telegram']['api_id']
    api_hash = config['telegram']['api_hash']
    username = config['telegram']['username']
    target_channel = config['Telegram']['target_channel']

    # Bot
    bot_token = config['telegram']['bot_token']

    # DB
    db_uri = config['mongodb']['uri']
    db_name = db_config['db_name']
    user_table_name = db_config['user_table_name']
    parsed_data_table_name = db_config['parsed_data_table_name']

    # Required instances
    event_manager = EventManager()
    bot = CustomBot(event_manager, bot_token, ui_config)
    db = DB(event_manager, db_uri, db_name, user_table_name, parsed_data_table_name)
    parser = Parser(event_manager, username, api_id, api_hash, target_channel)

    # Dispatcher
    dispatcher = Dispatcher(event_manager, bot, db, parser)
    asyncio.run(dispatcher.start())

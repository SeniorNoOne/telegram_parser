import logging
import time

import requests
import telebot
from telebot import TeleBot, types

from ui_elements import UIElements


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


telebot.apihelper.ENABLE_MIDDLEWARE = True


def log_function_call(func):
    def wrapper(*args, **kwargs):
        user = args[1].from_user

        logger.info(f"Calling function: {func.__name__}, user: {user.id}")
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper


def get_bot(token):
    tg_bot = Bot(token=token)
    return tg_bot


class Bot(TeleBot):
    ui_elements = UIElements
    
    def __init__(self, token, *args, **kwargs):
        self.bot = super().__init__(token, *args, **kwargs)
        self.target_words = []

        # Callback handlers
        self.message_handler(commands=['start'])(self.start_menu)

        self.message_handler(
            func=lambda message: message.text == 'Set target words')(self.add_target)

        self.message_handler(
            func=lambda message: message.text == 'Start parsing')(self.start_parsing)

        self.message_handler(
            func=lambda message: message.text == 'Pause parsing')(self.pause_parsing)

        self.message_handler(
            func=lambda message: message.text == 'Delete parsed info')(self.delete_parsed_info)

    def send_message_with_retries(self, chat_id, text, reply_markup=None,
                                  max_retries=3, retry_delay=2):
        retries = 0
        while retries < max_retries:
            try:
                response = self.send_message(chat_id, text, reply_markup=reply_markup)
                return response
            except requests.exceptions.RequestException as e:
                print(f"Request failed (Attempt {retries + 1}): {e}")
                retries += 1
                time.sleep(retry_delay)
        raise Exception(f"Max retries ({max_retries}) exceeded. Request failed.")

    @staticmethod
    def create_ui(buttons):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(button_name) for button_name in buttons]
        markup.add(*buttons)
        return markup

    @staticmethod
    def greeting_str(user):
        greeting_str = 'Hello, '
        greeting_str += f'{user.first_name} ' if user.first_name else ''
        greeting_str += f'{user.last_name}' if user.last_name else ''
        greeting_str += f'({user.username})' if user.username else ''
        return greeting_str

    @log_function_call
    def start_menu(self, message):
        ui_config = self.ui_elements['start_menu']
        markup = self.create_ui(ui_config['ui'])
        greeting_str = self.greeting_str(message.from_user)
        self.send_message_with_retries(
            message.chat.id,
            greeting_str + '\n\n' + ui_config['msg'],
            reply_markup=markup
        )

    @log_function_call
    def add_target(self, message):
        ui_config = self.ui_elements['add_target']
        markup = self.create_ui(ui_config['ui'])
        self.send_message_with_retries(message.chat.id, ui_config['msg'], reply_markup=markup)
        self.register_next_step_handler(message, self.process_target_input)

    @log_function_call
    def start_parsing(self, message):
        ui_config = self.ui_elements['start_parsing']
        if self.target_words:
            self.send_message_with_retries(message.chat.id, ui_config['msg'])
            return True
        else:
            self.send_message_with_retries(message.chat.id, ui_config['error_msg'])
            return False

    @log_function_call
    def pause_parsing(self, message):
        ui_config = self.ui_elements['start_parsing']
        self.send_message_with_retries(message.chat.id, ui_config['msg'])

    @log_function_call
    def delete_parsed_info(self, message):
        ui_config = self.ui_elements['delete_parsed_info']
        self.send_message_with_retries(message.chat.id, ui_config['msg'])

    @log_function_call
    def process_target_input(self, message):
        ui_config = self.ui_elements['process_target_input']

        if message.text.strip() == ui_config['exit_msg']:
            self.start_menu(message)
            return

        markup = self.create_ui(ui_config['ui'])

        response = ''
        target_words = []
        if message.content_type != 'text':
            response = ui_config['error_msg'] + message.content_type
        else:
            user_input = message.text.split(',')
            target_words = list(dict.fromkeys(user_input))

            if target_words:
                response = ui_config['msg'] + '\n'
                response += ', '.join(target_words)

        self.send_message_with_retries(message.chat.id, response, reply_markup=markup)
        self.register_next_step_handler(message, self.modify_target_words, target_words)

    @log_function_call
    def modify_target_words(self, message, target_words):
        append_cond, replace_cond = self.ui_elements['process_target_input']['ui']
        ui_config = self.ui_elements['modify_target_words']

        if message.text.strip() == append_cond:
            self.target_words.extend(target_words)
        elif message.text.strip() == replace_cond:
            self.target_words = target_words

        response = ui_config['msg'] + '\n'
        response += ', '.join(self.target_words)
        self.send_message_with_retries(message.chat.id, response)
        self.start_menu(message)


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read("config/config.ini")

    bot_token = config['Telegram']['bot_token']
    bot = get_bot(bot_token)

    bot.polling(none_stop=True, interval=0)

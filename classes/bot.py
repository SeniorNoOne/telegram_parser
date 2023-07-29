import asyncio
import configparser

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.ui_elements import UIElements
from utils.common import log_function_call

API_TOKEN = '6090729179:AAE_nnOWQBuI3R8-CkDTv7UuULN069tw1Bg'


class Form(StatesGroup):
    get_target_words = State()
    process_target_input = State()
    modify_target_words = State()


class CustomBot:
    ui_elements = UIElements

    def __init__(self, token, *args, **kwargs):
        self.bot = Bot(token=token, *args, **kwargs)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.storage = MemoryStorage()
        self.target_words = []

        self.dp.register_message_handler(self.start_menu, commands='start')
        self.dp.register_message_handler(self.get_target_words,
                                         Text(equals='Set target words', ignore_case=True),
                                         state=Form.get_target_words)
        self.dp.register_message_handler(self.process_target_words,
                                         state=Form.process_target_input)
        self.dp.register_message_handler(self.modify_target_words,
                                         Text(equals=('Append new words',
                                                      'Replace existing words'),
                                              ignore_case=True),
                                         state=Form.modify_target_words)

    @log_function_call
    async def start_menu(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['start_menu']
        markup = self.create_ui(ui_config['ui'])

        response = ui_config['msg']
        if message.text == '/start':
            response = self.greeting_str(message.from_user) + '\n\n' + ui_config['msg']

        await Form.get_target_words.set()
        await message.answer(response, reply_markup=markup)

    @log_function_call
    async def get_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['add_target']
        markup = self.create_ui(ui_config['ui'])

        await Form.process_target_input.set()
        await message.answer(ui_config['msg'], reply_markup=markup)

    @log_function_call
    async def process_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['process_target_input']
        markup = self.create_ui(ui_config['ui'])
        state = kwargs['state']

        response = ui_config['msg']
        target_words = []
        if message.content_type != 'text':
            response = ui_config['error_msg'] + message.content_type
        else:
            target_word_raw = message.text.split(',')
            target_words = list(dict.fromkeys(target_word_raw))
            response += '\n' + ', '.join(target_words)

        async with state.proxy() as data:
            data['name'] = target_words

        await Form.modify_target_words.set()
        await message.answer(response, reply_markup=markup)

    @log_function_call
    async def modify_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['modify_target_words']
        markup = self.create_ui(ui_config['ui'])
        state = kwargs['state']
        append_cond, replace_cond = self.ui_elements['process_target_input']['ui']

        async with state.proxy() as data:
            target_words = data['name']

        if message.text.strip() == append_cond:
            self.target_words.extend(target_words)
        elif message.text.strip() == replace_cond:
            self.target_words = target_words
        else:
            pass

        response = ui_config['msg'] + '\n'
        response += ', '.join(self.target_words)

        await state.finish()
        await message.answer(response, reply_markup=markup)
        await self.start_menu(message)

    async def start(self):
        await self.dp.start_polling()

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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    bot_token = config['Telegram']['bot_token']
    bot = CustomBot(bot_token)

    asyncio.run(bot.start())

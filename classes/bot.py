from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.common import log_function_call


class Form(StatesGroup):
    process_target_words = State()
    modify_target_words = State()


class CustomBot:
    def __init__(self, event_manager, token, ui_config, *args, **kwargs):
        self.event_manager = event_manager

        self.bot = Bot(token=token, *args, **kwargs)
        self.ui_elements = ui_config
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.register_message_handlers()

    def register_message_handlers(self):
        for method_name, parameters in self.ui_elements.items():
            message_handle_params = parameters['handlers']

            method = getattr(self, method_name)
            filters = message_handle_params['filters']
            commands = message_handle_params['commands']
            state = message_handle_params['state']

            if state == 'method_name':
                state = getattr(Form, method_name, state)

            if filters:
                filters = Text(filters, ignore_case=True)
                self.dp.register_message_handler(method, filters, commands=commands, state=state)
            else:
                self.dp.register_message_handler(method, commands=commands, state=state)

    @log_function_call
    async def start_handler(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['start_handler']
        markup = self.create_ui(ui_config['ui'])
        msg, *_ = ui_config['msg']

        if message.text == '/start':
            msg = self.greeting_str(message.from_user) + '\n\n' + msg

        user = self.user_from_message(message)
        self.event_manager.trigger_event('insert_user', user)

        await message.answer(msg, reply_markup=markup)

    @log_function_call
    async def cancel_handler(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['cancel_handler']
        markup = self.create_ui(ui_config['ui'])
        msg, *_ = ui_config['msg']
        state = kwargs['state']

        current_state = await state.get_state()
        if current_state:
            await state.finish()

        await message.answer(msg, reply_markup=markup)
        await self.start_handler(message)

    @log_function_call
    async def get_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['get_target_words']
        markup = self.create_ui(ui_config['ui'])
        msg, *_ = ui_config['msg']

        old_target_words = self.event_manager.trigger_event('fetch_target_words',
                                                            user_filter={'id': message.chat.id})

        if old_target_words:
            msg += '\n\nCurrent target words: ' + ', '.join(old_target_words)

        await Form.process_target_words.set()
        await message.answer(msg, reply_markup=markup)

    @log_function_call
    async def process_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['process_target_words']
        markup = self.create_ui(ui_config['ui'])
        msg, *_ = ui_config['msg']
        state = kwargs['state']

        target_words = []
        if message.content_type != 'text':
            msg = ui_config['error_msg'] + message.content_type
        else:
            target_word_raw = message.text.split(',')
            target_words = list(dict.fromkeys(target_word_raw))
            msg += '\n' + ', '.join(target_words)

        async with state.proxy() as data:
            data['name'] = target_words

        await Form.modify_target_words.set()
        await message.answer(msg, reply_markup=markup)

    @log_function_call
    async def modify_target_words(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['modify_target_words']
        markup = self.create_ui(ui_config['ui'])
        msg, *_ = ui_config['msg']
        state = kwargs['state']
        append_cond, replace_cond = ui_config['extras']

        # Getting target words from DB
        old_target_words = self.event_manager.trigger_event('fetch_target_words',
                                                            user_filter={'id': message.chat.id})
        # Getting new target words from bot storage
        async with state.proxy() as data:
            new_target_words = data['name']

        # Getting user form message and updating target words
        user = self.user_from_message(message)

        target_words = list(dict.fromkeys(new_target_words + old_target_words))
        if message.text.strip() == append_cond:
            user['target_words'].extend(target_words)
        elif message.text.strip() == replace_cond:
            user['target_words'] = target_words

        self.event_manager.trigger_event('update_target_words', user)

        msg += '\n' + ', '.join(target_words)

        await state.finish()
        await message.answer(msg, reply_markup=markup)
        await self.start_handler(message)

    @log_function_call
    async def start_parsing(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['start_parsing']
        markup = self.create_ui(ui_config['ui'])
        msg, error_msg, _ = ui_config['msg']

        if self.user_from_message(message):
            await self.event_manager.trigger_event('start_parser')
            await message.answer(msg, reply_markup=markup)
        else:
            await message.answer(error_msg, reply_markup=markup)

        await self.start_handler(message)

    @log_function_call
    async def pause_parsing(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['pause_parsing']
        markup = self.create_ui(ui_config['ui'])
        msg, error_msg, _ = ui_config['msg']

        if self.user_from_message(message):
            await self.event_manager.trigger_event('pause_parser')
            await message.answer(msg, reply_markup=markup)
        else:
            await message.answer(error_msg, reply_markup=markup)

        await self.start_handler(message)

    @log_function_call
    async def delete_parsed_info(self, message: types.Message, **kwargs):
        ui_config = self.ui_elements['delete_parsed_info']
        markup = self.create_ui(ui_config['ui'])
        msg, error_msg, _ = ui_config['msg']

        if user := self.user_from_message(message):
            self.event_manager.trigger_event('delete_user', user)
            await message.answer(msg, reply_markup=markup)
        else:
            await message.answer(error_msg, reply_markup=markup)

        await self.start_handler(message)

    async def start(self):
        await self.dp.start_polling()

    @staticmethod
    def create_ui(buttons):
        if buttons:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(button_name) for button_name in buttons]
            markup.add(*buttons)
        else:
            markup = types.ReplyKeyboardRemove()
        return markup

    @staticmethod
    def greeting_str(user):
        greeting_str = 'Hello, '
        greeting_str += f'{user.first_name} ' if user.first_name else ''
        greeting_str += f'{user.last_name}' if user.last_name else ''
        greeting_str += f'({user.username})' if user.username else ''
        return greeting_str

    @staticmethod
    def user_from_message(message):
        user = message.chat
        data = dict(user)
        data['target_words'] = []
        return data

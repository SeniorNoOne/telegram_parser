import re

from aiogram.types import ParseMode
from telethon import TelegramClient, events

from utils.common import logger, log_async_func


class Parser:
    def __init__(self, event_manager, username, api_id, api_hash,
                 target_channel_name, target_words):
        self.event_manager = event_manager

        # TG client connection credentials
        self.username = username
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None
        self.me = None

        # Flag to pause parsing process
        self.is_paused = True

        # Target channel and words
        self.target_channel_name = target_channel_name
        self.target_channel = None
        self.target_words = target_words

    @log_async_func
    async def start_parser(self):
        self.is_paused = False

    @log_async_func
    async def pause_parser(self):
        self.is_paused = True

    @log_async_func
    async def start(self):
        # Setting up client
        self.client = TelegramClient(self.username, self.api_id, self.api_hash)
        await self.client.start()
        logger.info('Client is started')

        # Setting up me
        self.me = await self.client.get_me()
        logger.info('Me is fetched')

        self.target_channel = await self.client.get_entity(self.target_channel_name)
        self.client.add_event_handler(self._new_message_handler,
                                      events.NewMessage(chats=self.target_channel))
        await self.client.run_until_disconnected()

    @log_async_func
    async def _new_message_handler(self, event):
        # Skipping if parsing process is stopped
        if self.is_paused:
            return

        message = event.message
        users = self.event_manager.trigger_event('fetch_users')

        for user in users:
            for target_word in user['target_words']:
                if re.match(target_word, message.text, flags=re.IGNORECASE):
                    post_link = f'https://t.me/c/{self.target_channel.id}/{message.id}/'

                    self.event_manager.trigger_event(
                        'insert_parsed_data',
                        {
                            'post_link': post_link,
                            'message': message.text,
                        }
                    )

                    msg = 'New message that you might be interested in has been posted\n\n'
                    msg += f'[Post link]({post_link})\n\n'
                    msg += 'Message content:\n' + message.text

                    await self.event_manager.trigger_event('notify_user', user['id'], msg,
                                                           parse_mode=ParseMode.MARKDOWN)
                    break

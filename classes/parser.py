import re

from telethon import TelegramClient, events

from utils.common import logger


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

        # Target channel and words
        self.target_channel_name = target_channel_name
        self.target_channel = None
        self.target_words = target_words

    async def start(self):
        self.client = TelegramClient(self.username, self.api_id, self.api_hash)
        await self.client.start()
        logger.info('Client is started')

        self.me = await self.client.get_me()
        logger.info('Me is fetched')

        self.target_channel = await self.client.get_entity(self.target_channel_name)

        self.client.add_event_handler(self._new_message_handler,
                                      events.NewMessage(chats=self.target_channel))

        await self.client.run_until_disconnected()

    async def _new_message_handler(self, event):
        message = event.message
        users = self.event_manager.trigger_event('fetch_users')

        for user in users:
            for target_word in user['target_words']:
                if re.match(target_word, message.text):
                    await self.event_manager.trigger_event('notify_user', user['id'], message.text)
                    break

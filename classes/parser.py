import re

from telethon import TelegramClient, events

from utils.common import logger


class Parser:
    def __init__(self, username, api_id, api_hash,
                 target_channel_name, target_words):
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
        messages = []

        @self.client.on(events.NewMessage(chats=self.target_channel))
        async def new_message_handler(event):
            message = event.message

            if any([re.match(pattern, message.text) for pattern in self.target_words]):
                messages.append(message.to_dict())
                # await self.bot.send_message(self.me.id, message.text)
                print(message.text)

        await self.client.run_until_disconnected()

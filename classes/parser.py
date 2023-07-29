import asyncio
import configparser

from re import match
from telethon import TelegramClient, events


class Parser:
    def __init__(self, event_handler, username, api_id, api_hash,
                 target_channel_name, target_words, tr_size=5, tr_timeout=600):
        self.event_handler = event_handler

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

        # DB conn parameters
        self.tr_size = tr_size
        self.tr_timeout = tr_timeout
        self.messages = []

    async def start(self):
        self.client = TelegramClient(self.username, self.api_id, self.api_hash)
        await self.client.start()
        print('Client is created')

        self.me = await self.client.get_me()
        print('Me is fetched')

        self.target_channel = await self.client.get_entity(self.target_channel_name)
        messages = []

        @self.client.on(events.NewMessage(chats=self.target_channel))
        async def new_message_handler(event):
            message = event.message

            if any([match(pattern, message.text) for pattern in self.target_words]):
                messages.append(message.to_dict())
                # await self.bot.send_message(self.me.id, message.text)
                print(message.text)

            # if len(messages) % transaction_size:
            #    collection.many(messages)

        await self.client.run_until_disconnected()


if __name__ == '__main__':
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    username = config['Telegram']['username']
    bot_token = config['Telegram']['bot_token']

    target_channel = 'https://t.me/test_parse_bot_1'
    target_words = ['.']
    transaction_size = 1

    parser = Parser(bot_token, username, api_id, api_hash,
                    target_channel, target_words,
                    transaction_size)

    asyncio.run(parser.start())

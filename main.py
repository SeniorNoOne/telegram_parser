import configparser
from re import match
from hashlib import sha256

from telethon import TelegramClient, events
from telegram import Bot

from db_conn import db


# Reading Configs
config = configparser.ConfigParser()
config.read("config/config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

username = config['Telegram']['username']
username_hash = sha256(username.encode('utf-8')).hexdigest()
bot_token = config['Telegram']['bot_token']

collection = db[username_hash]
transaction_size = 100

target_channel = ''
target_words = ['.']


async def main():
    bot = Bot(token=bot_token)
    print('Bot is started')

    client = TelegramClient(username, api_id, api_hash)
    await client.start()
    me = await client.get_me()
    print('Client is created')

    channel = await client.get_entity(target_channel)
    messages = []

    @client.on(events.NewMessage(chats=channel))
    async def new_message_handler(event):
        message = event.message

        if any([match(pattern, message.text) for pattern in target_words]):
            messages.append(message.to_dict)
            await bot.send_message(me.id, message.text)

        if len(messages) % transaction_size:
            collection.many(messages)

    await client.run_until_disconnected()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

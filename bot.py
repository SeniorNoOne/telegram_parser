import configparser

from telebot import TeleBot, types


config = configparser.ConfigParser()
config.read("config/config.ini")

bot_token = config['Telegram']['bot_token']
bot = TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def url(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Set target words')
    btn2 = types.KeyboardButton('Start parsing')
    btn3 = types.KeyboardButton('Stop parsing')
    btn4 = types.KeyboardButton('Delete private info')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'Choose an option', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Set target words')
def add_target(message):
    response = 'Enter target words to parse (comma separated)'
    bot.send_message(message.chat.id, response)
    bot.register_next_step_handler(message, process_target_input)


@bot.message_handler(func=lambda message: message.text == 'Delete private info')
def start_parsing(message):
    bot.send_message(message.chat.id, 'Started parsing')
    pass


@bot.message_handler(func=lambda message: message.text == 'Delete private info')
def stop_parsing(message):
    bot.send_message(message.chat.id, 'Stopped parsing')
    pass


@bot.message_handler(func=lambda message: message.text == 'Delete private info')
def delete_private_info(message):
    bot.send_message(message.chat.id, 'Private info deleted!')


def process_target_input(message):
    user_input = message.text
    target_words = [target.strip() for target in user_input.split(',')]

    if target_words:
        response = f'Target words used in parsing:\n'
        response += " ".join(target_words)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, 'Wrong input. Try again')


bot.polling(none_stop=True, interval=0)

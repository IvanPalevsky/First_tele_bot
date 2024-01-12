from config import token
import random
#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

jokes = ['Поймал старик золотую рыбку. '
        '— Отпусти меня, старче, три желания исполню! '
        '— Зашибись! — сказал старик. '
        'И зашиблась бедная рыбка, так и не исполнив два другие желания.',

        'Отец-охотник убил медведя. '
        'Мясо он оставил себе, шкуру подарил жене,'
        'а цирковой велосипед достался сыну.'
]

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello')


@bot.message_handler(commands=['random'])
def random_handler(message):
    n = random.randint(1, 100)
    bot.reply_to(message, f'случайное число - {n}')
    
@bot.message_handler(commands=['joke'])
def joke_handler(message):
    bot.reply_to(message, random.choice(jokes))


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    string = 'Ты сказал:' + message.text
    bot.reply_to(message, string)


bot.infinity_polling()
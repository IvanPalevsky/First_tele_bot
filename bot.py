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
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello')


@bot.message_handler(commands=['random'])
def random_handler(message):
    n = random.randint(1, 100)
    bot.reply_to(message, f'случайное число - {n}')
    
@bot.message_handler(commands=['joke'])
def joke_handler(message):
    bot.reply_to(message, random.choice(jokes))

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message)
    if "https://" in message: 
        chat_id = message.chat.id 
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.") 

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    string = 'Ты сказал:' + message.text
    bot.reply_to(message, string)


bot.infinity_polling()

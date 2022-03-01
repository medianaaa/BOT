import sqlite3
from telebot import types
from config import *


conn = sqlite3.connect('bot1.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, last_name: str, first_name: str, username: str):
    cursor.execute('INSERT OR IGNORE INTO test (user_id, last_name, first_name, username) VALUES (?, ?, ?, ?)',
                   [user_id, last_name, first_name, username])

    conn.commit()


keyboard = [
    [
        types.InlineKeyboardButton("Профиль", callback_data='button;1'),
        types.InlineKeyboardButton("Статистика", callback_data='button;2'),
]
]
b = types.InlineKeyboardMarkup(keyboard)

@bot.message_handler(commands=['start'])
def first(message):
    send = bot.send_message(message.chat.id, text='Привет!', reply_markup=b)
    bot.register_next_step_handler(send, profile)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button'))
def profile(call):
    button = call.data.split(';')
    if button[1] == '1':
        us_id = call.from_user.id
        la_name = call.from_user.first_name
        fi_name = call.from_user.last_name
        username = call.from_user.username

        UserID = '\nID: ' + str(us_id)
        LastName = '\nLast name:  ' + str(la_name)
        FistName = '\nFirst name:  ' + str(fi_name)
        UserName = '\nUser name:  ' + str(username)

        profile_message = 'Ваш профиль:\n' + UserID + LastName + FistName + UserName
        bot.send_message(us_id, profile_message)

        db_table_val(user_id=us_id, last_name=la_name, first_name=fi_name, username=username)

    elif button[1] == "2":
        for row in cursor.execute('SELECT COUNT(*) FROM test ORDER BY user_id'):
            bot.send_message(call.message.chat.id, row)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    ans = ''
    i = 0
    it = message.text[0]
    while it != ' ':
        i += 1
        ans += it
        it = message.text[i]
    bot.send_message(message.chat.id, ans)


if __name__ == '__main__':
    bot.polling(none_stop=True)
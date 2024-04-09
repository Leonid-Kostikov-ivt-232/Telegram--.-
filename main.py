import telebot
from telebot import apihelper
from telebot import types
import random
import logging

#apihelper.proxy = {'http': 'http://proxy.omgtu:8080','https':'http://proxy.omgtu:8080'}

API_TOKEN = '7157239291:AAHJxG2FWv-2Z76z4G_HRmJxL6YdFdh-JRw'
#API_TOKEN = '5969436163:AAG22C4iYDOScJ4U0WhPh8LA2O3SBKZgJeY'

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.INFO)

storage = dict()

def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)

def set_data_storage(user_id, key, value):
    storage[user_id][key] = value

def get_data_storage(user_id):
    return storage[user_id]

# Начало
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    btn2 = types.KeyboardButton("Об игре")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Добро пожаловать в игру 'Угадай число!'".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == "Начать игру":
        bot.register_next_step_handler(message, digitgames)
    elif message.text == "Об игре":
        bot.send_message(message.chat.id, """Бот загадывает любое число случайным образом и просит пользователя угадать это число.
Пользователь вводит число. Если его предположение неверно, то бот должен сказать, больше или меньше загаданное число,
а затем предложить пользователю повторить попытку. Если пользователь угадает число, игра считается завершенной.""")

# Игра "Угадай число"
def digitgames(message):

    init_storage(message.chat.id) # Инициализация хранилища

    attempt = 5
    set_data_storage(message.chat.id, "attempt", attempt)

    bot.send_message(message.chat.id, f'\nКоличество попыток: {attempt}')

    random_digit=random.randint(1, 10)
    print(random_digit)

    set_data_storage(message.chat.id, "random_digit", random_digit)
    print(get_data_storage(message.chat.id))
 
    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)

def process_digit_step(message):
    user_digit = message.text
    
    if not user_digit.isdigit():
        msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
        bot.register_next_step_handler(msg, process_digit_step)
        return

    attempt = get_data_storage(message.chat.id)["attempt"]
    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Вы угадали число! Это была цифра: {random_digit}')
        init_storage(message.chat.id) ### Очищает значения из хранилища
        return
    elif attempt > 1:
        attempt-=1
        set_data_storage(message.chat.id, "attempt", attempt)
        bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
        if int(user_digit) > random_digit:
            bot.send_message(message.chat.id, f'Число меньше {user_digit}!')
        elif int(user_digit) < random_digit:
            bot.send_message(message.chat.id, f'Число больше {user_digit}!')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Вы проиграли!')
        init_storage(message.chat.id) ### Очищает значения из хранилища
        return


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling()

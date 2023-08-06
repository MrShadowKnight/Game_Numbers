import telebot
from telebot import types
import random

bot = telebot.TeleBot("6558850363:AAGzAm67Fi7q5VuNGZbOIrL-INWVHZlVzqA")


def main_reply_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🎲Вгадай число"), types.KeyboardButton("Гра 2"))
    markup.row(types.KeyboardButton("Гра 3"))
    return markup


def r_sub_menu_numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("❓Правила"))
    markup.row(types.KeyboardButton("Легко"), types.KeyboardButton("Нормально"), types.KeyboardButton("Складно"))
    markup.row(types.KeyboardButton("Назад"))
    return markup


def random_numbers(random_number, user_input):
    cid = user_input.chat.id
    try:
        while user_input != random_number:
            new_msg = bot.register_next_step_handler(chat_id=cid)
            if user_input.text == "Стоп":
                bot.reply_to(cid, f"Ви не вгадали число.\nВашим числом було {random_number}")
                break
            if new_msg and new_msg.text.isdigit():
                user_input = int(new_msg.text)
            if user_input < random_number:
                bot.reply_to(cid, "Число менше від загаданого!\nПовторіть спробу:")
            elif user_input > random_number:
                bot.reply_to(cid, "Число більше від загаданого!\nПовторіть спробу:")


    except Exception as e:
        bot.reply_to(cid, f"Вітаю ви вгадали число!\nВоно {random_number}")


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "Привіт! Давай зіграємо гру!", reply_markup=main_reply_menu())


@bot.message_handler(commands=['help'])
def send_help(msg):
    bot.reply_to(msg, "Вибери гру і починай!")


@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    cid = msg.chat.id
    if msg.text == "🎲Вгадай число":
        bot.send_message(cid, "🎲", reply_markup=r_sub_menu_numbers())
    elif msg.text == "❓Правила":
        bot.send_message(cid,
                         "Правила\nВ цій грі треба вгадати число. І вона поділяється на складності:\nЛегка - від "
                         "1 до 10,\nНормальна - від 1 до 100\nСкладна - від 1 до 1000")
    elif msg.text == "Назад":
        bot.send_message(cid, "Назад", reply_markup=main_reply_menu())
    elif msg.text == "Легко":
        bot.reply_to(cid, "Ви почали гру. Введіть число:")
        random_number = random.randint(1, 10)
        random_numbers(random_number, msg)
    elif msg.text == "Нормально":
        bot.reply_to(cid, "Ви почали гру. Введіть число:")
        random_number = random.randint(1, 100)
        random_numbers(random_number, msg)
    elif msg.text == "Складно":
        bot.reply_to(cid, "Ви почали гру. Введіть число:")
        random_number = random.randint(1, 1000)
        random_numbers(random_number, msg)


bot.infinity_polling()

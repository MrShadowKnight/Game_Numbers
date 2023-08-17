import json
import telebot
from telebot import types
import random

bot = telebot.TeleBot("6558850363:AAGzAm67Fi7q5VuNGZbOIrL-INWVHZlVzqA")


def main_reply_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🎲Вгадай число"), types.KeyboardButton("❓Правила гри"))
    markup.row(types.KeyboardButton("📓Рахунок"))
    return markup


def r_sub_menu_numbers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Легко"), types.KeyboardButton("Нормально"), types.KeyboardButton("Складно"))
    markup.row(types.KeyboardButton("Назад"))
    return markup


def random_numbers(message, random_number):
    cid = message.chat.id
    try:
        if message.text == "Стоп" or message.text.lower == "Стоп":
            with open("note.json", "r") as file:
                note = json.load(file)
            for item in note:
                if cid == item['id']:
                    item['loss'] += 1
                    with open("note.json", "w") as file:
                        json.dump(note, file)
            return bot.send_message(cid,
                                    f"Ви не вгадали число.\nВашим числом було {random_number}.",
                                    reply_markup=r_sub_menu_numbers())
        user_number = int(message.text)
        if user_number < random_number:
            bot.send_message(cid, "Число менше від загаданого!\nПовторіть спробу:")
            bot.register_next_step_handler(message, random_numbers,
                                           random_number)
        elif user_number > random_number:
            bot.send_message(cid, "Число більше від загаданого!\nПовторіть спробу:")
            bot.register_next_step_handler(message, random_numbers,
                                           random_number)
        elif user_number == random_number:
            with open("note.json", "r") as file:
                note = json.load(file)
            for item in note:
                if cid == item['id']:
                    item['victory'] += 1
                    with open("note.json", "w") as file:
                        json.dump(note, file)
            bot.send_message(cid, f"Вітаю ви вгадали число!\nВоно {random_number}", reply_markup=r_sub_menu_numbers())
    except ValueError:
        bot.send_message(cid, "Повторіть спробу:")
        bot.register_next_step_handler(message, random_numbers,
                                       random_number)


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "Привіт! Давай зіграємо гру!", reply_markup=main_reply_menu())


@bot.message_handler(commands=['help'])
def send_help(msg):
    bot.reply_to(msg, "Вибери гру і починай!", reply_markup=main_reply_menu())


@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    try:
        cid = msg.chat.id
        with open("note.json", "r") as file:
            note = json.load(file)
        for item in note:
            if not any(item['id'] == cid for item in note):
                new_user = {
                    'id': cid,
                    'victory': 0,
                    'loss': 0
                }
                note.append(new_user)
        with open("note.json", "w") as file:
            json.dump(note, file)
    except Exception:
        cid = msg.chat.id
        count = [
            {
                'id': cid,
                'victory': 0,
                'loss': 0
            }
        ]
        with open("note.json", "w") as file:
            json.dump(count, file)
    finally:
        cid = msg.chat.id
        with open("note.json", "r") as file:
            note = json.load(file)
        if msg.text == "🎲Вгадай число":
            bot.send_message(cid, "🎲", reply_markup=r_sub_menu_numbers())
        elif msg.text == "❓Правила гри":
            bot.send_message(cid,
                             "Правила\nВ цій грі треба вгадати число. І вона поділяється на складності:\nЛегка - від "
                             "1 до 10,\nНормальна - від 1 до 100\nСкладна - від 1 до 1000")
        elif msg.text == "📓Рахунок":
            with open("note.json", "r") as file:
                note = json.load(file)
            for item in note:
                if item['id'] == cid:
                    bot.send_message(cid, f"Перемоги -- {item['victory']}\nПрограші -- {item['loss']}")
        elif msg.text == "Назад":
            bot.send_message(cid, "Назад", reply_markup=main_reply_menu())
        elif msg.text == "Легко":
            bot.send_message(cid, "Ви почали гру. Напишіть ,Стоп, для зупинки гри. Введіть число (1 - 10):")
            random_number = random.randint(1, 10)
            bot.register_next_step_handler(msg, random_numbers, random_number)
        elif msg.text == "Нормально":
            bot.send_message(cid, "Ви почали гру. Напишіть ,Стоп, для зупинки гри. Введіть число (1 - 100):")
            random_number = random.randint(1, 100)
            bot.register_next_step_handler(msg, random_numbers, random_number)
        elif msg.text == "Складно":
            bot.send_message(cid, "Ви почали гру. Напишіть ,Стоп, для зупинки гри. Введіть число (1 - 1000):")
            random_number = random.randint(1, 1000)
            bot.register_next_step_handler(msg, random_numbers, random_number)


bot.infinity_polling()

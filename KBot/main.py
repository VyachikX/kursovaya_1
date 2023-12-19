# -*- coding: utf-8 -*-

import telebot; #на телеботе весь чат-бот и работает (pip install pyTelegramBotAPI)
from KModules.config import Utils; #импорт библиотек, необходимых для работы бота
import requests; #импорт библиотеки запросов
import os.path; #системная библиотека для проверки наличия уже существующей базы данных


"""Основной код 
работы чат-бота"""


"""Подключение к Telegram API"""

bToken = Utils.token; #получение токена из конфигурационного файла
bot = telebot.TeleBot(bToken); #создание экземпляра класса

"""Определение команды /start"""
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, Utils.hello_message); #ответ бота на сообщение "/start" от пользователя

# Определение команды /help
@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, Utils.help_message); #ответ бота на сообщение "/help" от пользователя



# Определение команды /commands
@bot.message_handler(commands = ['commands'])
def send_comms(message):
    bot.reply_to(message, Utils.commands_message); #ответ бота на сообщение "/commands" от пользователя



# Определение команды /cats
@bot.message_handler(commands = ['cats'])
def send_cats(message):
    bot.reply_to(message, Utils.cats_message); #ответ бота на сообщение "/cats" от пользователя

# Определение команды /random
@bot.message_handler(commands = ['random'])
def send_random_place(message):
    try:
        bot.reply_to(message, "Сейчас я пришлю случайное памятное место в Смоленске!"); #отправка уведомления о том, что сейчас отправится случайное место
        if os.path.exists("KPlaces_k.db") == False:
            Utils.getData(); #дополнительный парсинг интересных мест Смоленска и помещение их в базу жанных
        data = Utils.getRandomData(); #SELECT случайное место из базы данных
        text = data[1] + "\n\n" + data[2] + "\n\n" + "Категория: " + data[4] + " (id места: " + str(data[0]) + ")"; #склеивание текста сообщения
        response = requests.get(data[3]); #подгогтовка фотографии
        photo_str = response.content; #для отправки пользователю
        bot.send_message(message.chat.id, text.replace("\t", "")); #отправка сообщения со случайным местом
        bot.send_photo(message.chat.id, photo_str); #отправка фото отдельно из-за большого описания
    except Exception as e:
        bot.reply_to(message, Utils.getErrorMessage(e)); #отправляем сообщение об ошибке пользователю

# Определение команды /. (команда для подвыборки по категории)
@bot.message_handler(commands = ['.'])
def get_category(message):
    list_to_send = []; #пустой список
    try:
        data = Utils.unpack_category(int(message.text.split()[1])); #запросик к базе, через модуль
        for i in data:
            list_to_send.append(i[1] + "\n" + "Для просмотра введите /! " + str(i[0])); #пополняем список данными
        bot.reply_to(message, "\n\n".join(list_to_send)); #отправляем сообщение пользователю
    except Exception as e:
        bot.reply_to(message, Utils.getErrorMessage(e)); #отправляем сообщение об ошибке пользователю

# Определение команды /! (команда для подвыборки по айди места)
@bot.message_handler(commands = ['!'])
def get_placeL(message):
    try:
        data = Utils.get_place(int(message.text.split()[1]))[0];
        response = requests.get(data[3]); #подгогтовка фотографии
        photo_str = response.content; #для отправки пользователю
        text = data[1] + "\n\n" + data[2] + "\n\n" + "Категория: " + data[4] + " (id места: " + str(data[0]) + ")"; #склеивание текста сообщения
        bot.send_message(message.chat.id, text); #отправка сообщения со случайным местом
        bot.send_photo(message.chat.id, photo_str); #отправка фото отдельно из-за большого описания
    except Exception as e:
        bot.reply_to(message, Utils.getErrorMessage(e)); #отправляем сообщение об ошибке пользователю
 

"""Непосредственный запуск бота в активный режим"""

bot.polling(none_stop = True); #старт

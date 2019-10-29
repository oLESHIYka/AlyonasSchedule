print("START...\n")

import sys
sys.path.append("./Includes")

import telebot
from telebot import apihelper

apihelper.proxy = {'https':'socks5://swcbbabh:aYEbh6q5gQ@dart.vivalaresistance.info:3306'}

# Конфигурация лога:
import logging
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', handlers=[logging.FileHandler(u'Logs/debugLog.log', 'w', 'utf-8')], level = logging.DEBUG)#, filename = u'Logs/debugLog.log')

import Token
import Constants

import MessegeParser

#c_testUserId = "777"
#MessegeParser.setUserSchedule(c_testUserId, MessegeParser.c_testMessage)
#print(MessegeParser.getAllSchedule(c_testUserId))
#MessegeParser.correctUserSchedule(c_testUserId, MessegeParser.c_testMessage2)


bot = telebot.TeleBot(Constants.c_telebotToken)

curCommand = Constants.Commands["NONE"]

def log(message, answer):
    logging.info("""
//==============================\\
    Сообщение от {0} {1} (id = {2}) 
    Текст: \"{3}\"
    Ответ: \"{4}\"
\\==============================//
    """.format(
        message.from_user.first_name
    ,   message.from_user.last_name
    ,   str(message.from_user.id)
    ,   message.text
    ,   answer
    ))

# ==============================================================================================
# Handlers:
@bot.message_handler(commands=["start"])
def startCommand_handler(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/start", "/help")
    user_markup.row("/задать", "/посмотреть", "/посмотреть_на")
    answer = "Давай создадим расписание 😊!"
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)
    log(message, answer)
    global curCommand
    curCommand = Constants.Commands["NONE"]

@bot.message_handler(commands=["help"])
def startCommand_handler(message):
    answer = """Тут будет большой и красивый help...
Но пока он не написан 😋"""
    bot.send_message(message.from_user.id, answer)
    log(message, answer)

@bot.message_handler(commands=["задать"])
def setSchedule_handler(message):
    global curCommand
    curCommand = Constants.Commands["SET"]
    answer = "Введите рассписание:"
    bot.send_message(message.from_user.id, answer)
    log(message, answer)

@bot.message_handler(commands=["посмотреть_на"])
def setSchedule_handler(message):
    answer = "Пока я не знаю как это, но скоро обязательно научюсь! 😋"
    bot.send_message(message.from_user.id, answer)
    log(message, answer)

@bot.message_handler(commands=["посмотреть"])
def setSchedule_handler(message):
    answer = MessegeParser.getAllSchedule(message.from_user.id)
    bot.send_message(message.from_user.id, answer, parse_mode="HTML")
    log(message, answer)

# ==============================================================================================
# Text:
@bot.message_handler(content_types=["text"])
def text_handler(message):
    global curCommand
    answer = ""
    user_id = message.from_user.id
    text = message.text

    if curCommand == Constants.Commands["SET"]:
        if MessegeParser.setUserSchedule(user_id, text):
            answer = "Расписание успешно задано!"
        else:
            answer = "Что-то пошло не так...\nПопробуйту ещё раз!"
    curCommand = Constants.Commands["NONE"]
    bot.send_message(user_id, answer)
    log(message, answer)

# ==============================================================================================
# Starting polling:
print("Starting polling...\n")
bot.polling(none_stop=True, interval=0)
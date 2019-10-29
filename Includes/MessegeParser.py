# ================================================================ #
# Файл MessageParser.py содержит в себе методы обаработки          #
# сообщений пользователя                                           #
# ================================================================ #

import re
import json
from jsonmerge import merge

import functools

c_testMessage = """Понедельник:
12-00: Вокал
14-00: Обед
Вторник:
8-00 - Подъём
ещё что-то
 бла бла бла
Среда: 
08-20: Подъем
9-00: Выход
18-00 Ужин
23-30 - Сон
Суббота:
12-12 что-то
11-45 последнее
"""

c_testMessage2 = """Вторник:
12-05 Вокал
14-00 Обед
23-30 Сон
Пятница:
8-20 встать!!!
22-00 лечь!!!
"""

c_daysKeyWords = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье "]
c_emptySchedule = [''] * len(c_daysKeyWords)

def ScheduleParser(text = c_testMessage):
    c_regexp = "^({0})\:\s*$".format("|".join(c_daysKeyWords))
    lastIdx = -1; lastKeyWord = ''
    res = c_emptySchedule
    for match in re.finditer(c_regexp, text, flags=re.MULTILINE):
        #if (lastIdx != -1):
        #    res[-1]['schedules'] = text[lastIdx:match.start()]
        #res.append({});
        #res[-1]['day'] = match[0]
        if lastKeyWord in c_daysKeyWords:
            res[c_daysKeyWords.index(lastKeyWord)] = text[lastIdx:match.start()].strip()
        lastIdx = match.end()
        lastKeyWord = match[1]

    if functools.reduce(lambda res, elem: res and ( elem == "" ), res, True): # Если все элементы пустые, значит пришли не валидные данные
        res = ''
        print("ERROR: Uexpected text Received!")
    else:
        res[c_daysKeyWords.index(lastKeyWord)] = text[lastIdx:].strip()

    return res

def writeDataToFile(data, path):
    print("\n__FUNCTION: writeDataToFile(data={0}, path={1})".format(data, path))
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    
def getDataFromFile(path):
    print("\n__FUNCTION: getDataFromFile(path={0})".format(path))
    res = []

    try:
        file = open(path, "r")
    except IOError as e:
        writeDataToFile(c_emptySchedule, path)
        return getDataFromFile(path)
    else:
        with file:
            return json.loads(file.read())
    
def generateFilePath(user_id):
    return "./Schedules/{0}.json".format(user_id)

#def compareObjects(base, corrections):
#    return

#def mergeData(base, corretions):
    

def getAllSchedule(user_id):
    path = generateFilePath(user_id)
    shedule = getDataFromFile(path)
    res = ""
    #for object in shedule:
    for idx in range(len(c_daysKeyWords)):
        curKeyWord = c_daysKeyWords[idx]
        curSchedule = shedule[idx]
        res += "\n" if idx > 0 else ""
        res += "<b>{0}:\n</b>{1}".format(curKeyWord,curSchedule)  #(object["day"], object["schedules"])
    return res

def setUserSchedule(user_id, text):
    print("\n__FUNCTION: setUserSchedule(user_id={0}, text={1})".format(user_id, text))
    path = generateFilePath(user_id)
    receivedData = ScheduleParser(text)
    if (len(receivedData) > 0):
        writeDataToFile(receivedData, path)
        return True
    else:
        return False

def correctUserSchedule(user_id, text):
    print("\n__FUNCTION: correctUserSchedule(user_id={0}, text={1})".format(user_id, text))
    path = generateFilePath(user_id)
    receivedData = ScheduleParser(text)
    if (len(receivedData) > 0):
        currentData = getDataFromFile(path)
        resData = merge(currentData, receivedData) # TO DO: Сделать нормальный merge
        writeDataToFile(resData, path)
        return True
    else:
        return False
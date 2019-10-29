# ================================================================ #
# Файл Constants.py предназначен для хранения глобальных констант  #
# ================================================================ #

c_startCommandMessage = "Давай создадим расписание 😊!"
c_helpCommandMessage = """Тут будет большой и красивый help...
Но пока он не написан 😋"""

from enum import Enum
Commands = Enum("Commands", "NONE START HELP SET GET GET_FOR")
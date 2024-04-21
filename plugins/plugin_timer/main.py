import sys
sys.path.append(r"../")

import asyncio
from num2words import num2words
from threading import Timer

import tts
from additions import *


female_units_min2 = (("минуту", "минуты", "минут"), "f")
female_units_min = (("минута", "минуты", "минут"), "f")
female_units_sec2 = (("секунду", "секунды", "секунд"), "f")
female_units_sec = (("секунда", "секунды", "секунд"), "f")
# female_units_uni = ((u'', u'', u''), 'f')

finish_sound = "plugins/plugin_timer/finish.mp3"



def main(cmd, phrase: str):
    phrase = phrase.replace("таймер ", "")

    if phrase == "":
        # таймер по умолчанию - на 5 минут
        txt = num2words(5, lang="ru")
        set_timer_real(5 * 60)
        return

    phrase += " "

    if phrase.startswith("на "):  # вырезаем "на " (из фразы "на Х минут")
        phrase = phrase[3:]

    # ставим секунды?
    for i in range(100, 1, -1):
        txt = num2words(i, lang="ru") + " " + "секунд "
        if phrase.startswith(txt):
            set_timer_real(i)
            return

        txt2 = num2words(i, lang="ru") + " " + "секунды "
        if phrase.startswith(txt2):
            set_timer_real(i)
            return

        txt3 = str(i) + " секунд "
        if phrase.startswith(txt3):
            set_timer_real(i)
            return

    # ставим минуты?
    for i in range(100, 1, -1):
        txt = num2words(i, lang="ru") + " " + "минуты "
        if phrase.startswith(txt):
            set_timer_real(i * 60)
            return

        txt2 = num2words(i, lang="ru") + " " + "минут "
        if phrase.startswith(txt2):
            set_timer_real(i * 60)
            return

        txt3 = str(i) + " минут "
        if phrase.startswith(txt3):
            set_timer_real(i * 60)
            return

    # без указания единиц измерения - ставим минуты
    for i in range(
        100, 1, -1
    ):  # обратный вариант - иначе "двадцать" находится быстрее чем "двадцать пять", а это неверно
        txt = num2words(i, lang="ru") + " "
        txt2 = num2words(i) + " "
        if phrase.startswith(txt2):
            set_timer_real(i * 60, txt)
            return

        txt3 = str(i) + " "
        if phrase.startswith(txt3):
            set_timer_real(i * 60)
            return

    # спецкейс под одну минуту
    if (
        phrase.startswith("один ")
        or phrase.startswith("одна ")
        or phrase.startswith("одну ")
    ):
        set_timer_real(1 * 60)
        return

    if phrase.startswith("две "):
        set_timer_real(2 * 60)
        return


def set_timer_real(num: int):
    tts.va_speak("время пошло")
    loop = asyncio.new_event_loop()
    Timer(num, loop.run_until_complete, (set_timer(num),)).start()
    # asyncio.run(set_timer(num))


def after_timer():
    tts.play_audio(finish_sound)
    # time.sleep(len(array) / smp_rt)
    tts.va_speak("Время вышло")
    return


async def set_timer(duration):
    print_text(duration)
    # time.sleep(duration)
    after_timer()

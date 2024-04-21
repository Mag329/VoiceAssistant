import sys

sys.path.append(r"../")
import tts
from additions import *

import requests
import pymorphy3
from num2words import num2words

from plugins.plugin_weather.config import api_key, base_city


morph = pymorphy3.MorphAnalyzer(lang="ru")


def main(cmd, text):
    TBR = ("в", "во")
    new_text = ""
    for word in text.split():
        if word in TBR:
            continue
        else:
            new_text += f"{word} "
    text += " текст текст текст"
    new_text = text
    text = text.split()
    if text[2] != "текст":
        city = text[2]
    else:
        city = base_city

    city = morph.parse(city)[0]
    city = city.normal_form

    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={api_key}"
        )
        data = response.json()

        city = data["name"]
        cur_temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        city = morph.parse(city)[0]
        city = city.inflect({"loct"}).word

        p = morph.parse("процент")[0]
        word = p.make_agree_with_number(humidity).word

        pressure = pressure * 0.7500637554192

        mm = morph.parse("миллиметр")[0]
        mm = mm.make_agree_with_number(pressure).word
        mm = mm.replace("миллим", "миллим+")

        metres = morph.parse("метр")[0]
        metres = metres.make_agree_with_number(wind).word

        text = f"Сейчас в {city} {num2words(int(cur_temp), lang='ru')}, {weather}, влажность {num2words(humidity, lang='ru')} {word}, давление {num2words(int(pressure), lang='ru')} {mm} ртутного столба, ветер {num2words(wind, lang='ru')} {metres} в секунду"

        print_text(text)
        tts.va_speak(text)

    except:
        tts.va_speak("Не удалось получить данные о погоде")

import plugins.plugin_shoplist.temp_data as temp_data

import sys

sys.path.append(r"../")
import tts
import config
from additions import *

from num2words import num2words
import pymorphy3
import json


morph = pymorphy3.MorphAnalyzer(lang="ru")

TBR = (
    "список",
    "покупок",
    "покупку",
    "товар",
    "добавь",
    "удали",
    "убери",
    "списка",
    "продуктов",
    "товаров",
)


def main(cmd, text):
    if text.startswith("добавь"):
        config.use_plugin = "shoplist"
        temp_data.product = ""

        for word in text.split():
            if word in TBR:
                continue
            else:
                temp_data.product += f"{word} "

        tts.va_speak("Назовите количество товара")

    elif text.startswith("очисть") or text.startswith("очисти"):
        with open("plugins/plugin_shoplist/list.json", encoding="utf8") as load_file:
            data = json.load(load_file)

        data["list"] = []

        with open("plugins/plugin_shoplist/list.json", "w", encoding="utf8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    elif text.startswith("что"):
        with open("plugins/plugin_shoplist/list.json", encoding="utf8") as load_file:
            data = json.load(load_file)

        speak = "Список покупок: "
        for i in data["list"]:
            try:
                speak += f'{i["name"]}, {num2words(i["amount"], lang="ru")}.'
            except:
                continue

        tts.va_speak(speak)

    # elif text.startswith('удали') or text.startswith('убери'):
    #     with open('plugins/plugin_shoplist/list.json', encoding='utf8') as load_file:
    #         load_data = json.load(load_file)
    #         product = ''
    #         for word in text.split():
    #             if word in TBR:
    #                 continue
    #             else:
    #                 product += f'{word} '
    #         print_text(product)
    #         # if product + ' ' in load_data['list']:
    #         try:
    #             load_data['list'][product].pop("name")
    #             load_data['list'][product].pop("amount")
    #             print_text(load_data)
    #         except:
    #             tts.va_speak(f'Не найдено')
    #             return

    #         tts.va_speak(f'{text}, удалено')

    #         print_text(load_data)
    #         with open('plugins/plugin_shoplist/list.json', 'w', encoding='utf8') as file:
    #             json.dump(load_data, file, ensure_ascii=False, indent=2)


def dialog(cmd, text):
    amount = ""
    for i in range(1, 100):
        txt = num2words(i, lang="ru") + " "
        if txt == text:
            amount = i
            break

    data = {"name": f"{temp_data.product}", "amount": f"{amount}"}

    with open("plugins/plugin_shoplist/list.json", encoding="utf8") as load_file:
        load_data = json.load(load_file)
        load_data["list"].append(data)

        print_text(load_data)
        with open("plugins/plugin_shoplist/list.json", "w", encoding="utf8") as file:
            json.dump(load_data, file, ensure_ascii=False, indent=2)

    config.use_plugin = None

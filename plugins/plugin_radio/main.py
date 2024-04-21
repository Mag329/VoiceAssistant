import sys

sys.path.append(r"../")
import config
import tts
from num2words import num2words
from additions import *

import vlc
import random
import time
import json
import asyncio

stations = {
    1: {"name": "радио дача", "url": "http://listen.vdfm.ru:8000/dacha"},
    2: {
        "name": "радио энэрджи",
        "url": "https://eu.stream4cast.com/proxy/energyfm/stream",
    },
    3: {
        "name": "дорожное радио",
        "url": "http://dorognoe.hostingradio.ru:8000/dorognoe",
    },
    4: {"name": "дип", "url": "https://radiorecord.hostingradio.ru/deep96.aacp"},
}

station_num = 1

is_playing = True

instance = vlc.Instance()
player = instance.media_player_new()

with open("config.json") as file:
    data = json.load(file)
    volume = data["main"]["volume"]
    volume = int(volume * 100)

next = ["дальше ", "следующее ", "следующая "]
stop = ["хватит ", "стоп "]

TBR = (
    "измени",
    "громкость",
    "звук",
    "звука",
    "воспроизведения",
    "музыки",
    "процентов",
    "процент",
    "процента",
    "по",
)

louder = "громче"
quieter = "тише"


def main(cmd, text):
    config.use_plugin = "radio"
    global station_num

    station_num = random.randint(1, len(stations))

    # text = text.replace("радио ", "")
    print_text(text)
    play_radio("play", player)


def dialog(cmd, text):
    if text in stop:
        config.use_plugin = None
        play_radio("stop", player)
        return

    elif text in next:
        global station_num
        station_num += 1
        if station_num > len(stations):
            station_num = 1
        play_radio("play", player)

    elif text in TBR:
        new_text = ""
        for word in text.split():
            if word in TBR:
                continue
            else:
                new_text += f"{word} "

        text = new_text

        if text in louder:
            volume = tts.volume + 0.1
            tts.set_volume(volume)
            return

        elif text in quieter:
            volume = tts.volume - 0.1
            tts.set_volume(volume)
            return

        elif text == "":
            volume = tts.volume * 10
            tts.va_speak(f"Громкость {volume}")

        else:
            for i in range(1, 101):
                txt = num2words(i, lang="ru") + " "
                if text == txt:
                    if i <= 10:
                        i = i / 10
                    elif i > 10 and i <= 100:
                        i = i / 100

                    tts.set_volume(i)
                    return


def set_volume(new_volume: int):
    global volume
    volume = int(new_volume * 100)
    play_radio("stop", player)
    player.audio_set_volume(volume)
    play_radio("play", player)


def play_radio(type, player):
    global is_playing

    if is_playing == True:
        stop_play()
        is_playing = False

    if type == "play":
        is_playing = True

        station = stations[station_num]

        tts.va_speak(f"  Играет {station['name']}")
        time.sleep(1)

        media = instance.media_new(station["url"])
        player.set_media(media)
        player.audio_set_volume(volume)
        player.play()

    elif type == "stop":
        stop_play()
        is_playing = False


def stop_play():
    global player
    player.stop()

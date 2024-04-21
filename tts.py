from speakerpy.lib_speak import Speaker
from speakerpy.lib_sl_text import SeleroText
import time
import json

import sounddevice as sd
import soundfile as sf

import config
from additions import *
import plugins


language = "ru"
model_id = "ru_v3"
sample_rate = 48000
speaker = "baya"  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yoo = True
device = "cpu"


with open("config.json") as file:
    data = json.load(file)
    volume = data["main"]["volume"]


def play_audio(file_path):
    # Загрузка аудиофайла
    data, sample_rate = sf.read(file_path)
    # Изменение громкости
    adjusted_data = data * volume
    # Воспроизведение
    sd.play(adjusted_data, sample_rate)
    sd.wait()


# Text to Speech
def va_speak(what: str):
    speaker = Speaker(
        model_id=model_id, language=language, speaker="baya", device=device
    )
    # time.sleep(len(audio) / sample_rate + 1)
    speaker.speak(what, sample_rate=sample_rate, put_accent=put_accent, put_yo=put_yoo)


def set_volume(new_volume: int):
    global volume
    if config.use_plugin == "radio":
        plugins.plugin_radio.main.set_volume(new_volume)
    volume = new_volume
    with open("config.json") as load_file:
        data = json.load(load_file)
        data["main"]["volume"] = volume
        with open("config.json", "w") as file:
            json.dump(data, file)
    print_text(volume)

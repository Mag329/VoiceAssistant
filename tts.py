from RUTTS import TTS
import sounddevice as sd
from ruaccent import RUAccent
import json
import config

from additions import *


model = 'TeraTTS/natasha-g2p-vits'

tts = TTS(model, add_time_to_end=0.8) 

accentizer = RUAccent()
accentizer.load(omograph_model_size='big_poetry', use_dictionary=True)

with open('config.json') as file:
    data = json.load(file)
    volume = data['main']['volume']


# def va_speak(what: str):
#     va_speak_async(what)
#     # asyncio.to_thread(va_speak_async(what))
#     # fix async func run from sync func
    

# Text to Speech
def va_speak(what: str):
    what = ' ' + what + ' ..'

    what = accentizer.process_all(what)
    print_text(what)
    
    audio = tts(what, lenght_scale=1.6)
    # tts.play_audio(audio)
    audio = audio * volume
    config.player = sd.play(audio, 24000)
    

def set_volume(new_volume: int):
    global volume
    volume = new_volume
    with open('config.json') as load_file:
        data = json.load(load_file)
        data['main']['volume'] = volume
        with open('config.json', 'w') as file:
            json.dump(data, file)
    print_text(volume)
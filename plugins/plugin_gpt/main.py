import sys
sys.path.append(r'../')
import tts
import config
from additions import *
from plugins.plugin_gpt import history

import g4f
import requests


def main(cmd, text):
    history.history = []
    tts.va_speak("В этом навыке вы можете общаться с нейрос+етью")
    
    config.use_plugin = 'gpt'


def dialog(cmd, text):
    question = text.replace('придумай ', '')
    if question == 'хватит ':
        history.history = []
        config.use_plugin = None
        return
    
    else:
        try:
            history.history.append({"role": "user", "content": question})
            response = ask(history.history)
            history.history.append({"role": "assistant", "content": response})
            print_text(response)
        except:
            response = "Ошибка генерации ответа"
        tts.va_speak(response)
    

def ask(message: str) -> str:
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_16k_0613,
            messages=message,
        )
        return response
        
         
    except requests.exceptions.RequestException as e:
        # if e.status_code == 403:
        print_error(f"Ошибка ответа сервера: \n{e}")
        return "Ошибка ответа сервера"
        
    except Exception as e:
        print_error(f"Ошибка генерации ответа: \n{e}")
        return "Ошибка генерации ответа"
    
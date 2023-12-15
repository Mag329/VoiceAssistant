import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import requests
import pymorphy3
import threading
import re
import time
from word2num.extractor import NumberExtractor

from OrangeHome import app
from OrangeHome.app import Devices, Commands
from smarthome import work_with_device, recognize_appliance


morph = pymorphy3.MorphAnalyzer(lang='ru')

print(f'Ассистент {config.VA_NAME} (v{config.VA_VER}) начал свою работу...')
# tts.va_speak('Слушаю ...')

def va_respond(voice: str):
    voice = input()
    if voice.startswith(config.VA_ALIAS):
        # print(voice)
        voice = filter_cmd(voice)
        cmd = recognize_cmd(voice)
        
        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak('Я вас не понимаю')
        else:
            execute_cmd(cmd['cmd'], voice)


# def filter_cmd(raw_voice: str):
#     cmd = raw_voice
    
#     for x in config.VA_ALIAS:
#         cmd = cmd.replace(x, '').strip()
        
#     for x in config.VA_TBR:
#         cmd = cmd.replace(x, '').strip()
        
#     print(cmd)
#     return cmd


# def filter_cmd(raw_voice: str):
#     cmd = raw_voice
    
#     for alias in config.VA_ALIAS:
#         cmd = re.sub(rf"\b{alias}\b", "", cmd)  

#     for x in config.VA_TBR:
#         cmd = re.sub(rf"\b{x}\b", "", cmd)
    
#     print(cmd.strip())
#     return cmd.strip()

def filter_cmd(raw_voice: str):
    cmd = raw_voice.split()
    
    filtered_cmd = ''
    
    for word in cmd:
        if word in config.VA_ALIAS or word in config.VA_TBR:
            continue
        else:
            filtered_cmd += f'{word} '
    
    print(filtered_cmd)
    return filtered_cmd
    

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd.split(), x)
            if vrt > rc['percent']:
            # if vrt > 20:
                rc['cmd'] = c
                rc['percent'] = vrt
    print(rc['cmd'])
    return rc


def execute_cmd(cmd: str, text):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        hour = morph.parse('час')[0]
        hour = hour.make_agree_with_number(now.hour).word
        minute = morph.parse('минута')[0]
        minute = minute.make_agree_with_number(now.minute).word
        text = f"Сейч+ас {num2words(now.hour, lang='ru')} {hour}, {num2words(now.minute, lang='ru')} {minute}"
        tts.va_speak(text)
        
    elif cmd == 'weather':
        print(text)
        text += ' текст текст текст'

        text = text.split()
        if text[3] != 'текст':
            city = text[3]
        else:
            city = 'москва'
            
        city = morph.parse(city)[0]
        city = city.normal_form
        
        api_key = "4af30c602f27cbcf2b342fafd86dfe60"
        
        try:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={api_key}")
            data = response.json()
            
            city = data['name']
            cur_temp = data['main']['temp']
            weather = data['weather'][0]['description']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            
            city = morph.parse(city)[0]
            city = city.inflect({'datv'}).word
            
            p = morph.parse('процент')[0]
            word = p.make_agree_with_number(humidity).word
            
            pressure = pressure *  0.7500637554192
            
            mm = morph.parse('миллиметр')[0]
            mm = mm.make_agree_with_number(pressure).word
            mm = mm.replace("миллим", "миллим+")
            
            text = f"Сейчас в {city} {num2words(int(cur_temp), lang='ru')}, {weather}, влажность {num2words(humidity, lang='ru')} {word}, давление {num2words(int(pressure), lang='ru')} {mm} ртутного столба, ветер {num2words(wind, lang='ru')} метров в секунду"
            
            tts.va_speak(text)
            
        except:
            tts.va_speak("Не удалось получить данные о погоде")
    
    elif cmd == 'on' or cmd == 'off':
        appliance = recognize_appliance(text)
        if appliance['type'] == 'device':
            appliance = appliance['device']
            
            # ip = Devices.query.filter_by(name=appliance).first().ip
            
            devices_db = Devices.query.filter().all()
            for device_db in devices_db:
                if device_db.name.lower() == appliance:
                    ip = device_db.ip
                    print(appliance, cmd, ip)
                    work_with_device(appliance, cmd, ip)
                else:
                    continue
                
            
        elif appliance['type'] == 'command':
            host = appliance['host']
            host = morph.parse(host)[0]
            host = host.normal_form
            command = appliance['command']
            device = appliance['device']
            
            devices_db = Devices.query.filter().all()
            for device_db in devices_db:
                if device_db.name.lower() == host:
                    ip = device_db.ip
                    print(host, device, ip)
                    work_with_device(host, device, ip)
                else:
                    continue
        else:
            return
        
    elif cmd == 'timer':
        seconds = text.split()[3]
        print(seconds)
        extractor = NumberExtractor()
        seconds = extractor.replace(seconds)
        print(seconds)
        timer = threading.Thread(target=timer, args=(seconds))
        timer.start()



def timer(time):
    tts.va_speak('Поставила таймер')
    time.sleep(time)
    

    
    
    
    

stt.va_listen(va_respond)
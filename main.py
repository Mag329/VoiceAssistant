import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import requests
import pymorphy3
import re

from OrangeHome import app
from OrangeHome.app import Devices, Commands


morph = pymorphy3.MorphAnalyzer(lang='ru')

print(f'Ассистент {config.VA_NAME} (v{config.VA_VER}) начал свою работу...')
# tts.va_speak('Слушаю ...')

def va_respond(voice: str):
    if voice.startswith(config.VA_ALIAS):
        print(voice)
        cmd = recognize_cmd(filter_cmd(voice))
        
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


def filter_cmd(raw_voice: str):
    cmd = raw_voice
    
    for alias in config.VA_ALIAS:
        cmd = re.sub(rf"\b{alias}\b", "", cmd)  

    for x in config.VA_TBR:
        cmd = re.sub(rf"\b{x}\b", "", cmd)
    
    print(cmd.strip())
    return cmd.strip()


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
            # if vrt > 80:
                rc['cmd'] = c
                rc['percent'] = vrt
    print(rc)
    return rc


def execute_cmd(cmd: str, text):
    if cmd == 'help':
        text = 'Я умею: ...'
        text += 'произносить время ...,'
        text += 'Рассказывать о погоде ...,'
        text += 'Управлять устройствами умного дома ...'
        tts.va_speak(text)
    
    elif cmd == 'ctime':
        now = datetime.datetime.now()
        hour = morph.parse('час')[0]
        hour = hour.make_agree_with_number(now.hour).word
        text = 'Сейч+ас ' + num2words(now.hour, lang='ru') + hour + num2words(now.minute, lang='ru') + ' мин+ут ...'
        tts.va_speak(text)
        
    elif cmd == 'weather':
        city = 'москва'
        
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
            
            text = f"Сейчас в {city} {num2words(int(cur_temp), lang='ru')}, {weather}, влажность {num2words(humidity, lang='ru')} {word}, давление {num2words(int(pressure), lang='ru')} миллим+етров ртутного столба, ветер {num2words(wind, lang='ru')} метров в секунду"
            
            tts.va_speak(text)
            
        except:
            tts.va_speak("Не удалось получить данные о погоде")
    
    elif cmd == 'on' or cmd == 'off':
        appliance = recognize_appliance(text)
        if appliance['type'] == 'device':
            appliance = appliance['device']
            work_with_device(appliance, cmd)
        else:
            device = appliance['device']
            device = morph.parse(device)[0]
            device = device.normal_form
            command = appliance['command']
            work_with_device(device, command)
        



    
# def recognize_appliance(text: str):
#     appliance = None
#     devices = Devices.query.order_by(Devices.id).all()
#     devices_name = [device.name.lower() for device in devices]
#     for word in text.split():
#         if word in devices_name:
#             appliance = word
#             break
            
#     if appliance:
#         return appliance
#     else:
#         tts.va_speak("Не удалось найти устройство")
#         return None

def recognize_appliance(text: str):
    devices = Devices.query.order_by(Devices.id).all()
    devices_name = [device.name.lower() for device in devices]
    commands = Commands.query.all()
    commands_name = [command.name.lower() for command in commands]
    if text.split()[2] in commands_name:
        command = text.split()[1]
        device = text.split()[-1]
        return {'type': 'command', 'device': device, 'command': command}
    elif text.split()[2] in devices_name:
        device = text.split()[2]
        return {'type': 'device', 'device': device}
    else:
        tts.va_speak("Не удалось найти устройство")
        return
        


def work_with_device(appliance: str, cmd: str):
    devices = Devices.query.order_by(Devices.id).all()
    for device in devices:
        if appliance == (device.name).lower():
            command = Commands.query.filter_by(device_id=device.id, name=cmd).first()
            if cmd == 'on': 
                tts.va_speak('Включаю ' + appliance)
                try:
                    requests.get(f'http://{device.ip}{command.command}')
                except requests.exceptions.ConnectionError:
                    tts.va_speak("Не удалось подключиться к устройству")
                except requests.exceptions.Timeout:
                    tts.va_speak("Таймаут запроса")
                except Exception as e:
                    tts.va_speak(f"Ошибка запроса: {e}")
            
            elif cmd == 'off':
                tts.va_speak('Выключаю ' + appliance)
                try:
                    requests.get(f'http://{device.ip}{command.command}')
                except requests.exceptions.ConnectionError:
                    tts.va_speak("Не удалось подключиться к устройству")
                except requests.exceptions.Timeout:
                    tts.va_speak("Таймаут запроса")
                except Exception as e:
                    tts.va_speak(f"Ошибка запроса: {e}")
    
    
def work_with_app(device: str, command: str):
    device_db = Devices.query.filter(name=device)
    command_db = Commands.query.filter(name=command)
    
    tts.va_speak('Включаю' + command)
    try:
        requests.get(f'http://{device_db.ip}{command_db.command}')
    except requests.exceptions.ConnectionError:
        tts.va_speak("Не удалось подключиться к устройству")
    except requests.exceptions.Timeout:
        tts.va_speak("Таймаут запроса")
    except Exception as e:
        tts.va_speak(f"Ошибка запроса: {e}")
    
    
    
    
    

stt.va_listen(va_respond)
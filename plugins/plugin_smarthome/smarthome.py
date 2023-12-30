import pymorphy3
import requests

import sys
sys.path.append(r'../../')
import tts
from additions import *
from OrangeHome.app import Devices, Commands


morph = pymorphy3.MorphAnalyzer(lang='ru')

CMD_ON = ('включи', 'вкл', 'запусти', 'вруби')
CMD_OFF = ('выключи', 'выкл', 'отключи', 'выруби')
TBR = ('на', 'в', 'у')

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
    new_text = ''
    for word in text.split():
        if word in CMD_ON or word in CMD_OFF or word in TBR:
            continue
        else:
            new_text += f'{word} '
    text = new_text

    
    devices = Devices.query.order_by(Devices.id).all()
    devices_name = [device.name.lower() for device in devices]
    commands = Commands.query.all()
    commands_name = [command.name.lower() for command in commands]
    
    names = text.split()[:-1]
    new_names = ''
    for name in names:
        name = morph.parse(name)[0]
        name = name.normal_form
        new_names += f'{name} '
        
    name = new_names.rstrip()
    if name == '':
        name = text
        name = morph.parse(name)[0]
        name = name.normal_form
        
    print_text(name)
    
    print_text(devices_name, commands_name)
    
    
    if name in commands_name:
        print_text(f'1{text}1')
        command = text.split()[:-1]
        print_text(f'2{command}2')
        device = name
        host = text.split()[-1]
        
        return {'type': 'command', 'device': device, 'command': command, 'host': host}
    elif name in devices_name:
        device = name
        
        return {'type': 'device', 'device': device}
    else:
        print_error('Не удалось найти устройство')
        tts.va_speak("Не удалось найти устройство")
        return {'type': 'None'}
        


def work_with_device(appliance: str, cmd: str, host: str):
    devices = Devices.query.order_by(Devices.id).all()
    for device in devices:
        if appliance == (device.name).lower():
            command = Commands.query.filter_by(device_id=device.id, name=cmd).first()
            if cmd == 'on':
                tts.va_speak('Включаю ')
                try:
                    requests.get(f'http://{host}{command.command}')
                except:
                    tts.va_speak("Не удалось подключиться к устройству")

            
            elif cmd == 'off':
                tts.va_speak('Выключаю ')
                try:
                    requests.get(f'http://{host}{command.command}')
                except:
                    tts.va_speak("Не удалось подключиться к устройству")

                    
            else:
                # command = Commands.query.filter_by(device_id=device.id, name=cmd).first()
                commands = Commands.query.filter().all()
                for command in commands:
                    if command.name.lower() == cmd and command.device_id == device.id:
                        tts.va_speak('Включаю ')
                        try:
                            print_text(f'http://{host}{command.command}')
                            requests.get(f'http://{host}{command.command}')
                        except:
                            tts.va_speak("Не удалось подключиться к устройству")
                        break
                    else:
                        continue
                else:
                    print_error('Не удалось найти устройство')
                    tts.va_speak('Не удалось найти устройство')
                    
                        

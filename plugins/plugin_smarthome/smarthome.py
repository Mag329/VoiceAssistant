import pymorphy3
import requests

import sys
sys.path.append(r'../../')
import tts
from OrangeHome.app import Devices, Commands


morph = pymorphy3.MorphAnalyzer(lang='ru')


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
    
    name = text.split()[1]
    name = morph.parse(name)[0]
    name = name.normal_form
    print(name)
    
    if name in commands_name:
        command = text.split()[1]
        device = name
        host = text.split()[-1]

        return {'type': 'command', 'device': device, 'command': command, 'host': host}
    elif name in devices_name:
        device = name
        
        return {'type': 'device', 'device': device}
    else:
        tts.va_speak("Не удалось найти устройство")
        return {'type': 'None'}
        


def work_with_device(appliance: str, cmd: str, host: str):
    devices = Devices.query.order_by(Devices.id).all()
    for device in devices:
        if appliance == (device.name).lower():
            command = Commands.query.filter_by(device_id=device.id, name=cmd).first()
            if cmd == 'on':
                name = morph.parse(appliance)[0]
                name = str(name.inflect({'accs'}).word)
                tts.va_speak('Включаю ' + name)
                try:
                    requests.get(f'http://{host}{command.command}')
                except:
                    tts.va_speak("Не удалось подключиться к устройству")

            
            elif cmd == 'off':
                name = morph.parse(appliance)[0]
                name = str(name.inflect({'accs'}).word)
                tts.va_speak('Выключаю ' + name)
                try:
                    requests.get(f'http://{host}{command.command}')
                except:
                    tts.va_speak("Не удалось подключиться к устройству")

                    
            else:
                # command = Commands.query.filter_by(device_id=device.id, name=cmd).first()
                commands = Commands.query.filter().all()
                for command in commands:
                    if command.name.lower() == cmd and command.device_id == device.id:
                        name = morph.parse(cmd)[0]
                        name = str(name.inflect({'accs'}))
                        tts.va_speak('Включаю ' + name)
                        try:
                            print(f'http://{host}{command.command}')
                            requests.get(f'http://{host}{command.command}')
                        except:
                            tts.va_speak("Не удалось подключиться к устройству")
                        break
                    else:
                        continue
                else:
                    tts.va_speak('Не удалось найти устройство')
                    
                        

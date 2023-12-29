import config
import stt
import tts
from fuzzywuzzy import fuzz
import pymorphy3
import os
import importlib
import sys
import time
import asyncio
from threading import Timer

from OrangeHome import app
# from plugins.plugin_telegram import main
import plugins


morph = pymorphy3.MorphAnalyzer(lang='ru')

print(f'Ассистент {config.VA_NAME} (v{config.VA_VER}) начал свою работу...')

def va_respond(voice):
    asyncio.run(va_respond_async(voice))
    

async def va_respond_async(voice: str):
    voice = input()
    if voice != None:
        if voice.startswith(config.VA_ALIAS):
            # print(voice)
            voice = filter_cmd(voice)
            cmd = recognize_cmd(voice)
            
            if config.use_plugin != None:
                execute_cmd(config.use_plugin, voice, 'dialog')
            
            else:
                if cmd['cmd'] not in config.VA_CMD_LIST.keys() or cmd['percent'] < 50:
                    tts.va_speak('Я вас не понимаю')
                    
                    # spec = importlib.util.spec_from_file_location('main', (os.path.join(f'plugins/plugin_gpt/main.py')))
                    # plugin = importlib.util.module_from_spec(spec)
                    
                    # sys.modules['plugin_gpt'] = plugin
                    # spec.loader.exec_module(plugin)
                    
                    # plugin.main(cmd, voice)
                else:
                    try:
                        print(f"Command: {cmd['cmd']}, Percent: {cmd['percent']}")
                        execute_cmd(cmd['cmd'], voice)
                    except:
                        tts.va_speak('ошибка навыка')
                    
                    # config.is_active = True
                    # print(config.is_active)
                    # loop = asyncio.new_event_loop()
                    # Timer(30, loop.run_until_complete, (is_active_off(),)).start()




    

async def is_active_off():
    # time.sleep(30)
    config.is_active = False
    print(config.is_active)


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
    for cmd in cmd.split():
        for c, v in config.VA_CMD_LIST.items():
            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > rc['percent']:
                # if vrt > 40:
                    rc['cmd'] = c
                    rc['percent'] = vrt
    return rc


def execute_cmd(cmd: str, text, func='main'):
    functions = config.VA_CMD_FUNCS
    
    plugin_name = 'plugin_' + functions[cmd]
    plugin_path = os.path.join(f'plugins/{plugin_name}/main.py')
    
    if not os.path.exists(plugin_path):
        print(f'Plugin {plugin_name} not found')
        return
    
    spec = importlib.util.spec_from_file_location('main', plugin_path)
    plugin = importlib.util.module_from_spec(spec)
    
    sys.modules[plugin_name] = plugin
    spec.loader.exec_module(plugin)
    
    if func == 'main':
        plugin.main(cmd, text)
    elif func == 'dialog':
        plugin.dialog(cmd, text)
    
    
    
    
# main.start
stt.va_listen(va_respond)

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
from additions import *


morph = pymorphy3.MorphAnalyzer(lang='ru')

loop = None
timer = None

print_text(f'Ассистент {config.VA_NAME} (v{config.VA_VER}) начал свою работу...')

def va_respond(voice):
    asyncio.run(va_respond_async(voice))
    

async def va_respond_async(voice: str):
    voice = input()
    if voice != None:
        if voice.startswith(config.VA_ALIAS) or config.is_active:
            voice = filter_cmd(voice)
            cmd = recognize_cmd(voice)
            
            if config.use_plugin != None:
                execute_cmd(config.use_plugin, voice, 'dialog')
            
            else:
                if cmd['cmd'] not in config.functions_list.keys() or cmd['percent'] < 50 and not config.is_active:
                    if config.player == None:
                        tts.va_speak('Я вас не понимаю')
                    else:
                        config.player.stop()
                        config.player = None
                    
                    # spec = importlib.util.spec_from_file_location('main', (os.path.join(f'plugins/plugin_gpt/main.py')))
                    # plugin = importlib.util.module_from_spec(spec)
                    
                    # sys.modules['plugin_gpt'] = plugin
                    # spec.loader.exec_module(plugin)
                    
                    # plugin.main(cmd, voice)
                else:
                    if config.player != None:
                        config.player.stop()
                        config.player = None
                        if cmd['cmd'] == 'stop':
                            return
                        
                    print_text(f"Command: {cmd['cmd']}, Percent: {cmd['percent']}")
                    execute_cmd(cmd['cmd'], voice)
                    
                    global timer
                    global loop
                    
                    if timer != None:
                        timer.cancel()
                        timer = None
                    if loop != None:
                        loop.stop()
                        loop = None
                    
                    config.is_active = True
                    print_text(config.is_active)
                    loop = asyncio.new_event_loop()
                    timer = Timer(15, loop.run_until_complete, (is_active_off(),))
                    timer.start()




    

async def is_active_off():
    # time.sleep(30)
    config.is_active = False
    print_text(config.is_active)


def filter_cmd(raw_voice: str):
    cmd = raw_voice.split()
    
    filtered_cmd = ''
    
    for word in cmd:
        if word in config.VA_ALIAS or word in config.VA_TBR:
            continue
        else:
            filtered_cmd += f'{word} '
    
    print_text(filtered_cmd)
    return filtered_cmd
    

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for cmd in cmd.split():
        for c, v in config.functions_list.items():
            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > rc['percent']:
                # if vrt > 40:
                    rc['cmd'] = c
                    rc['percent'] = vrt
    return rc


def execute_cmd(cmd: str, text, func='main'):
    plugin_name = 'plugin_' + cmd
    plugin_path = os.path.join(f'plugins/{plugin_name}/main.py')
    
    if not os.path.exists(plugin_path):
        print_text(f'Plugin {plugin_name} not found')
        return
    
    spec = importlib.util.spec_from_file_location('main', plugin_path)
    plugin = importlib.util.module_from_spec(spec)
    
    sys.modules[plugin_name] = plugin
    spec.loader.exec_module(plugin)
    
    if func == 'main':
        plugin.main(cmd, text)
    elif func == 'dialog':
        plugin.dialog(cmd, text)
    
    
    
    
# Загрузка плагинов
plugins = []
for name in os.listdir('plugins/'):
    if name.startswith('plugin_'):
        plugins.append(name)
        
for plugin in plugins:
    name = plugin.replace('plugin_', '')
    if not os.path.exists(f'plugins/{plugin}/commands.py'):
        print_error(f'CMD_NAMES not found in plugin {name} ')
        continue
    commands_module = importlib.import_module(f'plugins.{plugin}.commands')
   
    config.functions_list[name] = commands_module.CMD_NAMES
   

stt.va_listen(va_respond)

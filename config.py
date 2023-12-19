VA_NAME = 'Алиса'

VA_VER = "1.1"

VA_ALIAS = ('алиса')

VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько', 'поставь', 'какая', 'подбрось', 'брось', 'рандомное', 'случайное', 'давай')

VA_CMD_LIST = {
    "on": ('включи', 'вкл', 'запусти', 'вруби'),
    "off": ('выключи', 'выкл', 'отключи', 'выруби'),
    "ctime": ('время', 'текущее время', 'сейчас времени', 'который час'),
    "timer": ('таймер'),
    "weather": ('погода', 'погодка', 'прогноз погоды'),
    # "random": ('рандом', 'рандомное число', 'случайное число', 'монетку', 'кубик', 'монетка'),
    "gpt": ('спроси у нейросети', 'придумай', 'придумаем'),
}

VA_CMD_FUNCS = {
    "on": 'smarthome',
    "off": 'smarthome',
    "ctime": 'ctime',
    "timer": 'timer',
    "weather": 'weather',
    "random": 'random',
    "gpt": 'gpt',
}



use_plugin = None # !!! НЕ ИЗМЕНЯТЬ !!!
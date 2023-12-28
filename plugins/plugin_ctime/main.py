import sys
sys.path.append(r'../')
import tts

from num2words import num2words
import datetime
import pymorphy3


morph = pymorphy3.MorphAnalyzer(lang='ru')

def main(cmd, text):
    now = datetime.datetime.now()
    hour_word = morph.parse('час')[0]
    hour_word = hour_word.make_agree_with_number(now.hour).word
    
    minute_word = morph.parse('минута')[0]
    minute_word = minute_word.make_agree_with_number(now.minute).word
    minute_word = minute_word.replace('минут', 'мин+ут')
    text = f"Сейч+ас {num2words(now.hour, lang='ru')} {hour_word}, {num2words(now.minute, lang='ru')} {minute_word}"
    tts.va_speak(text)
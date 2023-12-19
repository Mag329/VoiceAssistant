import sys
sys.path.append(r'../')
import tts

from num2words import num2words
import random
import pymorphy3


morph = pymorphy3.MorphAnalyzer(lang='ru')

def main(cmd, text):
    text = text.split()[0]
    text = morph.parse(text)[0].normal_form
    
    if text == 'кубик':
        results = [
            "Выпала один",
            "Выпало два",
            "Выпало три",
            "Выпало четыре",
            "Выпало пять",
            "Выпало шесть",
        ]
        tts.va_speak(results[random.randint(0, len(results) - 1)])
        
    elif text == 'монетка':
        results = [
            "выпал oрёл",
            "выпала решка",
        ]
        
        tts.va_speak(results[random.randint(0, len(results) - 1)])
        
    elif text == 'число' or text == 'ранд':
        tts.va_speak(f"выпало {num2words(random.randint(1, 100), lang='ru')}")
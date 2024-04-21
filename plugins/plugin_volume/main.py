import sys

sys.path.append(r"../")
import tts

import pymorphy3
from num2words import num2words


morph = pymorphy3.MorphAnalyzer()

TBR = (
    "измени",
    "громкость",
    "звук",
    "звука",
    "воспроизведения",
    "музыки",
    "процентов",
    "процент",
    "процента",
    "по",
)

louder = "громче"
quieter = "тише"


def main(cmd, text):
    new_text = ""
    for word in text.split():
        if word in TBR:
            continue
        else:
            new_text += f"{word} "

    text = new_text

    if text in louder:
        volume = tts.volume + 0.1
        tts.set_volume(volume)
        return

    elif text in quieter:
        volume = tts.volume - 0.1
        tts.set_volume(volume)
        return

    elif text == "":
        volume = tts.volume * 10
        tts.va_speak(f"Громкость {volume}")

    else:
        for i in range(1, 101):
            txt = num2words(i, lang="ru") + " "
            if text == txt:
                if i <= 10:
                    i = i / 10
                elif i > 10 and i <= 100:
                    i = i / 100

                tts.set_volume(i)
                return

import sys

sys.path.append(r"../")
import tts
from additions import *


TBR = ("повтори", "скажи")
GREETINGS = ("передай", "привет", "поздоровайся")


def main(cmd, text):
    new_text = ""
    for word in text.split():
        if word in TBR:
            continue
        else:
            new_text += f"{word} "

    text = new_text

    for word in text.split():
        if word in GREETINGS:
            type = "hello"
            break
        else:
            type = "other"
            break

    print_text(text)
    print_text(type)

    if type == "hello":
        for word in text.split():
            if word in GREETINGS:
                text = text.replace(word, "")

        print_text(f"передаю привет {text}")
        tts.va_speak(f"передаю привет {text}")

    else:
        tts.va_speak(text)

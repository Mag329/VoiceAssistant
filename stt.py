import vosk
import sys
import sounddevice as sd
import queue
import json

from additions import *


model = vosk.Model("model")
samplerate = 16000
device = "hw:2,0"

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print_text(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        device=device,
        dtype="int16",
        channels=1,
        callback=q_callback,
    ):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            # else:
            #     print_text(rec.PartialResult())

import torch
import sounddevice as sd
import time


language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'xenia' # aidar, baya, kseniya, xenia, random
put_accent = True
put_yoo = True
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


# Text to Speech
def va_speak(what: str):
    '''
        ## Озвучка текста

        ### Params:
        - what: Текст для озвучки
        
        ### Return:
        - None
    '''
    what += ' .....'
    if 'кого-' in what:
        what = what.replace('кого-', 'ково-')
    audio = model.apply_tts(text=what,
                        speaker=speaker,
                        sample_rate=sample_rate,
                        put_accent=put_accent,
                        put_yo=put_yoo)
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 1)
    sd.stop()
    

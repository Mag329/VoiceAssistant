from RUTTS import TTS
import sounddevice as sd
from ruaccent import RUAccent


model = 'TeraTTS/natasha-g2p-vits'

tts = TTS(model, add_time_to_end=0.8) 

accentizer = RUAccent()
accentizer.load(omograph_model_size='big_poetry', use_dictionary=True)

volume = 0.5

# Text to Speech
def va_speak(what: str):
    '''
        ## Озвучка текста

        ### Params:
        - what: Текст для озвучки
        
        ### Return:
        - None
    '''
    # what += '...'

    what = accentizer.process_all(what)
    print(what)
    
    audio = tts(what, lenght_scale=1.4)
    # tts.play_audio(audio)
    audio = audio * volume
    print(volume)
    sd.play(audio, 24000)
    

def set_volume(new_volume: int):
    '''
        ## Установка громкости

        ### Params:
        - volume: Громкость от 0 до 10
        
        ### Return:
        - None
    '''
    global volume
    volume = new_volume
    print(volume)
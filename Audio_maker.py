from gtts import gTTS
import os

def convert(text):
    gTTS(text=text).save("welcome.mp3")
    os.system("welcome.mp3")

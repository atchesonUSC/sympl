import os
from gtts import gTTS


class Speaker:
    def __init__(self):
        self.filename = '~/output.mp3'

    def speak(self, text):
        tts = gTTS(text)
        tts.save(self.filename)
        os.system(f'start {self.filename}')


def main():
    text1 = 'test one'
    text2 = 'test two'

    filename = 'tts.mp3'
    tts = gTTS(text1)
    tts.save(filename)

    os.system(f'start {filename}')

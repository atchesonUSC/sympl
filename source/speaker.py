from gtts import gTTS
import os


class Speaker:
    def __init__(self):
        self.filename = '~/tts.mp3'

    def speak(self, text):
        tts = gTTS(text)
        tts.save('tts.mp3')

        os.system(f'start {self.filename}')


def main():
    text1 = 'test one'
    # text2 = 'test two'

    filename = 'tts.mp3'
    tts = gTTS('hello world')
    tts.save(filename)

    os.system(f'start {filename}')
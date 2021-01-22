import sys
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def setup_pins():
    # Specify pin numbering system
    # BOARD = 1, 2, 3, etc.
    # BCM = GPIO1, GPIO7, etc.
    GPIO.setmode(GPIO.BOARD)

    # Disable pin configuration warnings
    GPIO.setwarnings(False)

    # Setup output channel
    chan_list = [28]
    GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)


def select_device(chan):
    time.sleep(0.1)
    GPIO.output(chan, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(chan, GPIO.HIGH)


def main():
    setup_pins()
    rfid = SimpleMFRC522()

    try:
        arg = input('Read tag? (y/n): ')
        
        if arg == 'y':
            select_device(28)
            code, text = rfid.read()
            print('[Data] {}  |  {}'.format(code, text)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()


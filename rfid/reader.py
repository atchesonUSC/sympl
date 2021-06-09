import os
import signal
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


"""
============================================
*                 Readers                  *
============================================
*
* rfid_0 -> GPIO_8 (physical 24) -> device_0
* rfid_1 -> GPIO_7 (physical 26) -> device_1
* rfid_2 -> GPIO_6 (physical 31) -> device_2
*
--------------------------------------------
"""


def exit_handler(sig, frame):
    print('\n[Exit Signal Received]')
    GPIO.cleanup()
    os._exit(0)

def main():
    # Setup readers
    rfid_0 = SimpleMFRC522(dev=0)
    rfid_1 = SimpleMFRC522(dev=1)
    rfid_2 = SimpleMFRC522(dev=2)

    try:
        rfid = input('RFID: ')
        if rfid == '0':
            code, text = rfid_0.read()
            print('Code: {}\nText: {}'.format(code, text))
        elif rfid == '1':
            code, text = rfid_1.read()
            print('Code: {}\nText: {}'.format(code, text))
        elif rfid == '2':
            code, text = rfid_2.read()
            print('Code: {}\nText: {}'.format(code, text))
        elif rfid == 'a':
            code0, text0 = rfid_0.read()
            code1, text1 = rfid_2.read()
            print('Code0: {}\nText0: {}'.format(code0, text0))
            print('Code1: {}\nText1: {}'.format(code1, text1))
        else:
            print('Try again...')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    main()


import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


# def setup_pins():
#     # Specify pin numbering system
#     # BOARD = 1, 2, 3, etc.
#     # BCM = GPIO1, GPIO7, etc.
#     GPIO.setmode(GPIO.BOARD)
#
#     # Disable pin configuration warnings
#     #GPIO.setwarnings(False)
#
#     # Setup output channel
#     GPIO.setup(chan, GPIO.OUT, initial=GPIO.HIGH)


# def select_device(rfid):
#     # Set the channel LOW
#     GPIO.output(chan, GPIO.LOW
#     time.sleep(0.1)
#
#     # Read from the sensor
#     code,text = rfid.read()
#     print(code)
#     print(text)
#
#     # Set the channel HIGH
#     GPIO.output(chan, GPIO.HIGH)
#     time.sleep(0.1)


"""
Readers
=======
* rfid_0 -> GPIO_8 -> device_0
* rfid_2 -> GPIO_6 -> device_2
"""


def main():
    rfid_0 = SimpleMFRC522()
    rfid_2 = SimpleMFRC522()

    try:
        rfid = int(input('RFID: '))
        if rfid == 0:
            code, text = rfid_0.read()
            print('Code: {}\nText: {}'.format(code, text))
        elif rfid == 2:
            code, text = rfid_2.read()
            print('Code: {}\nText: {}'.format(code, text))
        else:
            print('Try again...')
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()


import sys
import time
import spidev
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


#spi = spidev.SpiDev()
#spi.open(0, 0)
#spi.no_cs = False


chan = 31


def setup_pins():
    # Specify pin numbering system
    # BOARD = 1, 2, 3, etc.
    # BCM = GPIO1, GPIO7, etc.
    GPIO.setmode(GPIO.BOARD)

    # Disable pin configuration warnings
    #GPIO.setwarnings(False)

    # Setup output channel
    GPIO.setup(chan, GPIO.OUT, initial=GPIO.HIGH)


def select_device(rfid):
    # Set the channel LOW
    GPIO.output(chan, GPIO.LOW)
    time.sleep(0.1)
    
    # Read from the sensor
    code,text = rfid.read()
    print(code)
    print(text)
    
    # Set the channel HIGH
    GPIO.output(chan, GPIO.HIGH)
    time.sleep(0.1)


def main():
    setup_pins()
    rfid = SimpleMFRC522()

    try:
        print('Reading...')
        select_device(rfid)
    except KeyboardInterrupt:
        print('Interrupted')
        #spi.close()
    finally:
    #    spi.close()
        GPIO.cleanup()


if __name__ == '__main__':
    main()


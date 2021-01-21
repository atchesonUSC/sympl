import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

rfid = SimpleMFRC522()

try:
  print("[STATUS] Place tag for reading...")
  code, text = rfid.read()
  print('[DATA] {}  |  {}'.format(code, text))

finally:
  GPIO.cleanup()

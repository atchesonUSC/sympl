import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

rfid = SimpleMFRC522()

try:
  data = input("[STATUS] Enter data to write: ")
  print("[STATUS] Place tag for writing...")
  rfid.write(data)
  print("[STATUS] Data written successfully!")

finally:
  GPIO.cleanup()

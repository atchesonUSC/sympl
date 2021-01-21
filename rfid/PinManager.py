"""
This class is to handle all interactions with the RFID sensors
"""

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


class RFID:
    def __init__(self, rfid, num_readers):
        self.__rifd = rfid
        self.__sz = num_readers

    def acquire(self, block_id):

    """
    This function will individual activate the chip select for
    each reader and collect data.
    """
    def read(self):
        blocks = []

        for i in range(0, self.__sz):
            ...
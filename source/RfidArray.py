import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


class RfidArray:
    def __init__(self, size):
        self.size = size

        self.readers = []
        for i in range(0, size):
            self.readers.append(SimpleMFRC522(dev=i))

    def read(self):
        block_code = []
        for reader in self.readers:
            tag_id, code = reader.read()
            block_code.append(code)
        return block_code

class Block:
    def __init__(self, block_data, block_type):
        self.type = block_type
        self.data = block_data

    def get_type(self):
        return self.type

    def get_data(self):
        return self.data

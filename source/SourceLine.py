class SourceLine:

    def __init__(self, line_num, indents):
        self.indents = indents
        self.line_num = line_num
        self.data = []

    # add code fragment to the source code line
    def insert(self, fragment):
        self.data.append(fragment)

    def printline(self):
        print(self.data)

    def get_indents(self):
        return self.indents

    def get_data(self):
        return self.data

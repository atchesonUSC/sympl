class SourceLine:

    def __init__(self, l, i, t):
        self.indents = i
        self.line_num = l
        self.data = []

    # add code fragment to the source code line
    def append(self, fragment):
        self.data.append(fragment)

    def get_indents(self):
        return self.indents

    def get_data(self):
        return self.data

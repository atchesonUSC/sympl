class SourceLine:

    def __init__(self, l, i, t):
        self.indents = i
        self.line_num = l
        self.type = t
        self.data = []

    # add code fragment to the source code line
    def append(self, fragment):
        self.data.append(fragment)

    def process(self):
        line = self.indents * '\t'
        for block in self.data:
            if block.get_type() == 'delimiter':
                if block.get_delimiter_type() == 'end-condition':
                    line += ':'
            else:
                line += block.get_data() + ' '
        return line

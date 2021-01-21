"""
=================================================================================================================
* [parser.py]: This file houses the Parser class definition, which handles parsing block code into *
*                     Python source code (uses containers).                                                     *
=================================================================================================================
"""


import containers


class Parser:
    def __int__(self, blocks):
        self.i = 0
        self.blocks = blocks

    """
    [FUNCTION]: format_number()
    """
    def format_number(self):
        number = self.blocks[self.i]

        # look at next block
        self.i += 1

        # keep building out number if multiple digits
        while self.blocks[self.i].isnumeric():
            number += self.blocks[self.i]
            self.i += 1

    """
    [FUNCTION]: format_variable()
    """
    def format_variable(self):
        return 0

    """
    [FUNCTION]: format_if()
    """
    def format_if(self):
        return 0

    """
    [FUNCTION]: format_loop()
    """
    def format_loop(self):
        return 0

    """
    [FUNCTION]: format_assignment()
    """
    def format_assignment(self):
        return 0

    """
    [FUNCTION]: format_arithmetic()
    """
    def format_arithmetic(self):
        return 0

    """
    [FUNCTION]: format_comparator()
    """
    def format_comparator(self):
        return 0

    """
    [FUNCTION]: parse()
    """
    def parse(self):
        return 0

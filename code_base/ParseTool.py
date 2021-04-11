"""
=================================================================================================================
* [ParseTool.py]: This file houses the Parser class definition, which handles parsing block code into *
*                     Python source code (uses containers).                                                     *
=================================================================================================================
"""


from SourceLine import SourceLine


class Stack:
    def __init__(self):
        self.data = []

    def size(self):
        return len(self.data)

    def empty(self):
        if self.size() > 0:
            return True
        else:
            return False

    def top(self):
        if self.empty():
            return 0
        else:
            return self.data[-1]

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.empty():
            return 0
        else:
            x = self.data[-1]
            del self.data[-1]
            return x

    def clear(self):
        while self.top() != 'if':
            if not self.empty():
                self.pop()
            else:
                raise Exception('[ERROR] Reached end of condition stack')
        self.pop()


class ParseTool:
    def __init__(self, block_code):
        # current index in block_code
        self.i = 0

        # block code data
        self.block_code = block_code

        # indentation tracker for source code file
        self.line_num = 0
        self.indents = 0

        # stores the processed source lines
        self.processed = []

        # keep track of conditional branching
        self.stack = Stack()

    def format_assign(self, blocks):
        operators = ['=', '+', '-', '*', '/']

        # create source line
        srcline = SourceLine(self.line_num, self.indents, 'assign')

        # set left-exp
        srcline.append(blocks[self.i])
        srcline.append(blocks[self.i+1])
        self.i += 2

        # set prev
        prev = 'assign'

        while True:
            if self.i >= len(blocks):
                raise Exception('[ERROR] Started assignment but no end found')

            # update curr
            curr = blocks[self.i]
            
            if (curr.isalpha() or curr.isdigit()) and (prev == 'assign' or prev in operators):
                self.i += 1
                pass
            elif (curr in operators) and (prev.isdigit() or prev.isalpha()):
                self.i += 1
                pass
            elif (curr == 'end') and (prev.isdigit() or prev.isalpha()):
                if len(blocks) > self.i:
                    ondeck = blocks[self.i+1]
                    if ondeck == 'elif' or ondeck == 'else' or ondeck == 'end-conditional-structure' or\
                            ondeck == 'end-loop':
                        self.indents -= 1
                    if ondeck == 'end-conditional-structure' or ondeck == 'end-loop':
                        self.i += 2
                        break
                    if ondeck == 'end-conditional-structure':
                        self.stack.clear()
                    else:
                        self.i += 1
                        break
            else:
                raise Exception('[ERROR] Incorrect block after assign')

            # add to source line
            srcline.append(curr)

            # update prev
            prev = curr

        # add to processed list
        self.processed.append(srcline)
        self.line_num += 1

    def format_if_elif(self, blocks):
        operators = ['=', '+', '-', '*', '/']
        comparators = ['<', '>']

        # set curr and prev
        prev = blocks[self.i]
        curr = None
        if len(blocks) > self.i+1:
            curr = blocks[self.i+1]
        else:
            raise Exception('[ERROR] Incomplete loop condition')

        # push branch onto stack
        if (prev == 'elif') and (self.stack.empty()):
            raise Exception('[ERROR] Can\'t create \'elif\' branch as first branch in branching sequence')
        elif (prev == 'elif') and (self.stack.top() == 'else'):
            raise Exception('[ERROR] Can\'t create \'elif\' branch as first branch in branching sequence')
        else:
            self.stack.push(prev)

        # create source line
        srcline = SourceLine(self.line_num, self.indents, prev)

        # tracks if we've already seen a comparator
        comp_flag = False

        while True:
            if curr.isdigit() or curr.isalpha():
                if (prev == 'if') or (prev == 'elif') or (prev in comparators) or (prev in operators):
                    if self.i+1 < len(blocks)-1:
                        if blocks[self.i+1] in comparators:
                            if (prev not in comparators) and (not comp_flag):
                                srcline.append(curr)
                                self.i += 1

                                # update prev and curr
                                prev = curr
                                curr = blocks[self.i]
                            else:
                                raise Exception('[ERROR] Can\'t use more than one comparator in a condition')
                        elif blocks[self.i+1] in operators:
                            srcline.append(curr)
                            self.i += 1

                            # update prev and curr
                            prev = curr
                            curr = blocks[self.i]
                        elif blocks[self.i+1] == 'end':
                            srcline.append(curr)
                            self.i += 1
                            break
                        else:
                            raise Exception('[ERROR] Incorrect block after number or variable')
                    else:
                        raise Exception('[ERROR] Missing an \'end-condition\' block')
            elif curr in operators:
                if prev.isdigit() or prev.isalpha():
                    if self.i < len(blocks)-2:
                        if blocks[self.i+1].isdigit() or blocks[self.i+1].isalpha():
                            srcline.append(curr)
                            self.i += 1

                            # update prev and curr
                            prev = curr
                            curr = blocks[self.i]
                        else:
                            raise Exception('[ERROR] Incorrect block following an operator')
                    else:
                        raise Exception('[ERROR] Incomplete expression to right of operator')
                else:
                    raise Exception('[ERROR] Incorrect block before operator')
            elif curr in comparators:
                if not comp_flag:
                    if prev.isdigit() or prev.isalpha():
                        if self.i < len(blocks)-2:
                            if blocks[self.i+1].isdigit() or blocks[self.i+1].isalpha():
                                srcline.append(curr)
                                self.i += 1

                                # update prev and curr
                                prev = curr
                                curr = blocks[self.i]

                                # set comp flag
                                comp_flag = True
                            else:
                                raise Exception('[ERROR] Incorrect block following a comparator')
                        else:
                            raise Exception('[ERROR] Incomplete expression to right of condition comparator')
                    else:
                        raise Exception('[ERROR] Incorrect block before comparator')
                else:
                    raise Exception('[ERROR] Can\'t ues more than one comparator in a condition')
            else:
                raise Exception('[ERROR] Incorrect block - not a block used for conditions')

        # add to processed list
        self.processed.append(srcline)
        self.line_num += 1

        # update indentation
        self.indents += 1

    def format_else(self, blocks):
        # set prev and curr
        prev = blocks[self.i-1]
        curr = blocks[self.i]

        # push branch onto stack
        if self.stack.top() == 'if' or self.stack.top() == 'elif':
            self.stack.push(curr)
        else:
            raise Exception('[ERROR] An \'if\' or \'elif\' branch should come before an \'else\' branch')

        # create source line
        srcline = SourceLine(self.line_num, self.indents, 'else')

        if self.i > 0:
            if prev == 'end':
                if len(blocks) > self.i+1:
                    ondeck = blocks[self.i+1]
                    if ondeck.isdigit() or ondeck.isalpha() or ondeck == 'end' or ondeck == 'end-conditional-structure':
                        srcline.append(curr)
                        self.i += 1
                    else:
                        raise Exception('[ERROR] Incorrect block following an \'else\'')
                else:
                    raise Exception('[ERROR] \'Else\' branch is incomplete')
            else:
                raise Exception('[ERROR] Incorrect block before an \'else\' branch')
        else:
            raise Exception('[ERROR] \'else\' is not connected to an \'elif\' or \'if\' branch')

        # added to processed list
        self.processed.append(srcline)
        self.line_num += 1

        # update indents
        self.indents += 1

    def format_loop(self, blocks):
        # create source line
        srcline = SourceLine(self.line_num, self.indents, 'loop')

        # set up curr and prev
        prev = blocks[self.i]
        curr = None
        if len(blocks) > self.i+1:
            curr = blocks[self.i+1]
        else:
            raise Exception('[ERROR] Incomplete loop condition')

        # update position
        self.i += 1

        while True:
            if curr.isdigit() or curr.isalpha():
                if len(blocks) > self.i+1:
                    ondeck = blocks[self.i+1]
                    if ondeck == 'end':
                        srcline.append(curr)
                        self.i += 2
                        break
                    else:
                        raise Exception('[ERROR] Incorrect for closing a loop condition')
            else:
                raise Exception('[ERROR] Incorrect block following a \'loop\' block')

        # add to processed list
        self.processed.append(srcline)
        self.line_num += 1

        # update indents
        self.indents += 1

    def preprocess(self):
        i = 0
        proc = []
        while i < len(self.block_code):
            if not self.block_code[i].isdigit():
                proc.append(self.block_code[i])
                i += 1
            else:
                num = self.block_code[i]
                i += 1
                while self.block_code[i].isdigit():
                    num += self.block_code[i]
                proc.append(num)
        return proc

    def create_tree(self):
        variables = ['a', 'b', 'c', 'x', 'y', 'z']
        conditionals = ['if', 'elif', 'else']
        looping = ['loop']

        """
        * [Stage]: Pre-processing
        * [Desc]: Iterate over the list of block and concatenate adjacent digits into single numbers,
                return a list of block data with numbers concatenated.
        """
        proc = self.preprocess()

        """
        * [Stage]: Processing
        * [Desc]: Iterate over list of block data and create abstract syntax trees out of block data.
        """
        try:
            while self.i < len(proc):
                curr = proc[self.i]
                if curr in variables:
                    if proc[self.i + 1] == '=':
                        self.format_assign(proc)
                    else:
                        raise Exception('[ERROR] Incorrect element following Variable')
                elif curr in conditionals:
                    if curr == 'if':
                        self.format_if_elif(proc)
                    elif curr == 'elif':
                        self.format_if_elif(proc)
                    else:
                        self.format_else(proc)
                elif curr in looping:
                    self.format_loop(proc)
                else:
                    raise Exception('[ERROR] Incorrect beginning to a line of code')
        except Exception as e:
            print(e)

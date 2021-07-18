"""
=================================================================================================================
* [ParseTool.py]: This file houses the Parser class definition, which handles parsing block code into           *
*                 Python code, which will get written to the output.py file.                                    *
=================================================================================================================
"""


from SourceLine import SourceLine


class Stack:
    def __init__(self, stack_type):
        self.data = []

        # stack types: 'branch' (track branch delimiters) or 'loop' (track loop delimiters)
        self.type = stack_type

    def size(self):
        return len(self.data)

    def empty(self):
        return self.size() == 0

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
            tmp = self.data[-1]
            del self.data[-1]
            return tmp

    def clear(self):
        if self.type == 'branch':
            if self.empty():
                raise Exception('[ERROR] Reached end of branch stack')
            else:
                while self.top() != 'if' and not self.empty():
                    self.pop()
                if self.top() == 'if':
                    self.pop()
                else:
                    raise Exception('[ERROR] Reached end of branch stack')
        else:
            if self.empty():
                raise Exception('[ERROR] Reached end of loop stack')
            else:
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

        # keeps track of conditional branching and loop formatting
        self.branch_stack = Stack('branch')
        self.loop_stack = Stack('loop')

    def format_assign(self, blocks):
        operators = ['=', '+', '-', '*', '/']

        # create source line
        srcline = SourceLine(self.line_num, self.indents)
        srcline.insert(blocks[self.i])
        if len(blocks) <= self.i+1:
            raise Exception('[ERROR] Too few blocks in assignment')
        srcline.insert(blocks[self.i+1])
        self.i += 2

        # set prev
        prev = '='

        while True:
            if self.i >= len(blocks):
                raise Exception('[ERROR] Started assignment but no end block found')

            # update curr
            curr = blocks[self.i]
            
            if (curr.isalpha() or curr.isdigit()) and (prev == '=' or prev in operators):
                self.i += 1
                srcline.insert(curr)
                pass
            elif (curr in operators) and (prev.isdigit() or prev.isalpha()):
                self.i += 1
                srcline.insert(curr)
                pass
            elif (curr == 'end') and (prev.isdigit() or prev.isalpha()):
                if self.i+1 < len(blocks):
                    ondeck = blocks[self.i+1]
                    if ondeck == 'elif' or ondeck == 'else' or ondeck == 'end-conditional-structure' or ondeck == 'end-loop':
                        self.indents -= 1
                    if ondeck == 'end-conditional-structure' or ondeck == 'end-loop':
                        self.i += 2
                        if ondeck == 'end-conditional-structure':
                            self.branch_stack.clear()
                        else:
                            self.loop_stack.clear()
                        break
                    else:
                        self.i += 1
                        break
                elif self.i+1 == len(blocks):
                    self.i += 1
                    break
                else:
                    raise Exception('[ERROR] Incorrect assignment operation format')
            else:
                raise Exception('[ERROR] Incorrect assignment operation format')

            # update prev
            prev = curr

        # add to processed list
        self.processed.append(srcline)
        self.line_num += 1

    def format_if_elif(self, blocks):
        operators = ['=', '+', '-', '*', '/']
        comparators = ['<', '>']

        # set curr and prev
        if self.i+1 >= len(blocks):
            raise Exception('[ERROR] Incomplete branch condition condition')
        prev = blocks[self.i]
        curr = blocks[self.i+1]

        # push branch onto stack
        if (prev == 'elif') and (self.branch_stack.empty()):
            raise Exception('[ERROR] Can\'t create \'elif\' branch as first branch in branching sequence')
        elif (prev == 'elif') and (self.branch_stack.top() == 'else') or self.branch_stack.empty():
            raise Exception('[ERROR] Can\'t create \'elif\' branch as first branch in branching sequence')
        self.branch_stack.push(prev)

        # create source line
        srcline = SourceLine(self.line_num, self.indents)

        # tracks if we've already seen a comparator
        comp_flag = False

        while True:
            if self.i >= len(blocks):
                raise Exception('[ERROR] Incomplete branch condition')

            if curr.isdigit() or curr.isalpha():
                if (prev == 'if') or (prev == 'elif') or (prev in comparators) or (prev in operators):
                    if self.i+1 <= len(blocks)-1:
                        ondeck = blocks[self.i+1]
                        if ondeck in comparators:
                            if not comp_flag:
                                srcline.insert(curr)
                                self.i += 1

                                # update prev and curr
                                prev = curr
                                curr = blocks[self.i]
                            else:
                                raise Exception('[ERROR] Can\'t use more than one comparator in a condition')
                        elif ondeck in operators:
                            srcline.insert(curr)
                            self.i += 1

                            # update prev and curr
                            prev = curr
                            curr = blocks[self.i]
                        elif ondeck == 'end':
                            srcline.insert(curr)
                            self.i += 1
                            break
                        else:
                            raise Exception('[ERROR] Incorrect block after number or variable')
                    else:
                        raise Exception('[ERROR] Missing an \'end-condition\' block')
                else:
                    raise Exception('[ERROR] Incorrect branch condition')
            elif curr in operators:
                if prev.isdigit() or prev.isalpha():
                    if self.i+1 <= len(blocks)-1:
                        ondeck = blocks[self.i+1]
                        if ondeck.isdigit() or ondeck.isalpha():
                            srcline.insert(curr)
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
                        if self.i+1 <= len(blocks)-1:
                            ondeck = blocks[self.i+1]
                            if ondeck.isdigit() or ondeck.isalpha():
                                srcline.insert(curr)
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
                    raise Exception('[ERROR] Can\'t use more than one comparator in a condition')
            else:
                raise Exception('[ERROR] Incorrect block - not a block used for conditions')

        # append semi-colon
        srcline.insert(':')

        # add to processed list
        self.processed.append(srcline)
        self.line_num += 1

        # update indentation
        self.indents += 1

    def format_else(self, blocks):
        # set prev and curr
        if self.i-1 < 0:
            raise Exception('[ERROR] An \'if\' or \'elif\' branch should come before an \'else\' branch')
        prev = blocks[self.i-1]
        curr = blocks[self.i]

        # push branch onto stack
        if self.branch_stack.top() == 'if' or self.branch_stack.top() == 'elif':
            self.branch_stack.push(curr)
        else:
            raise Exception('[ERROR] An \'if\' or \'elif\' branch should come before an \'else\' branch')

        # create source line
        srcline = SourceLine(self.line_num, self.indents)

        if prev == 'end':
            if len(blocks) > self.i+1:
                ondeck = blocks[self.i+1]
                if ondeck.isdigit() or ondeck.isalpha():
                    srcline.insert(curr)
                    self.i += 1
                elif ondeck == 'end-conditional-structure':
                    srcline.insert(curr)
                    self.indents -= 1
                    self.i += 2
                    self.branch_stack.clear()
                else:
                    raise Exception('[ERROR] Incorrect block following an \'else\'')
            else:
                raise Exception('[ERROR] \'Else\' branch is incomplete')
        else:
            raise Exception('[ERROR] Incorrect block before an \'else\' branch')

        # append semi-colon
        srcline.insert(':')

        # added to processed list
        self.processed.append(srcline)
        self.line_num += 1

        # update indents
        self.indents += 1

    def format_loop(self, blocks):
        # create source line
        srcline = SourceLine(self.line_num, self.indents)
        srcline.insert(blocks[self.i])

        # push 'loop' notice onto loop stack
        self.loop_stack.push(blocks[self.i])

        # set up curr and prev
        if len(blocks) <= self.i+1:
            raise Exception('[ERROR] Incomplete loop condition')
        curr = blocks[self.i+1]

        # update position
        self.i += 1

        while True:
            if self.i >= len(blocks):
                raise Exception('[ERROR] Incomplete loop condition')

            if curr.isdigit() or curr.isalpha():
                if len(blocks) > self.i+1:
                    ondeck = blocks[self.i+1]
                    if ondeck == 'end':
                        srcline.insert(curr)
                        self.i += 2
                        break
                    else:
                        raise Exception('[ERROR] Incorrect for closing a loop condition')
                else:
                    raise Exception('[ERROR] Incomplete loop condition')
            else:
                raise Exception('[ERROR] Incorrect block following a \'loop\' block')

        # append semi-colon
        srcline.insert(':')

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
                while i <= len(self.block_code) and self.block_code[i].isdigit():
                    num += self.block_code[i]
                    i += 1
                proc.append(num)
        return proc

    def parse(self):
        variables = ['a', 'b', 'c', 'x', 'y', 'z']
        branching = ['if', 'elif', 'else']
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
                    if self.i+1 <= len(proc):
                        if proc[self.i+1] == '=':
                            self.format_assign(proc)
                        else:
                            raise Exception('[ERROR] Incorrect element following variable')
                    else:
                        raise Exception('[ERROR] Incomplete assignment operation')
                elif curr in branching:
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

        '''
        * [Stage]: Scope check
        * [Desc]: Scan for correct scoping of variables. Raise exception if incorrect.
        try:
            ...
        except Exception as e:
            print(e)
        '''

    # returns a list of formatted source lines, which can be written to source file, which can be executed
    def format_srclines(self):
        variables = ['a', 'b', 'c', 'x', 'y', 'z']
        formatted_lines = []

        for line in self.processed:
            # srcline string to be written to output.py file
            tmp = ''

            # append line elements
            tabs = '    ' * line.get_indents()
            tmp += tabs

            i = 0
            data = line.get_data()
            if data[i] == 'loop':
                tmp += 'for i in range(0, ' + data[1] + '):'
            elif data[i] in variables or data[i] == 'if' or data[i] == 'elif' or data[i] == 'else':
                while i < len(data):
                    tmp += data[i] + ' '
                    i += 1

            # append line to formatted_lines
            formatted_lines.append(tmp)

        return formatted_lines

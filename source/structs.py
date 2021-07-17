"""
Assignment:
* left-exp
* right-exp

Operation:
* left-exp
* right-exp
* operator

If Statement:
* condition
* body

Elif Statement:
* condition
* body

Else:
* body

Loop:
* condition
* body
"""


class Assign:
    def __init__(self, indents):
        self.indents = indents
        self.type = 'assign'
        self.left = None
        self.right = None

    def set_left(self, exp):
        self.left = exp

    def set_right(self, exp):
        self.right = exp


class Variable:
    def __init__(self, val):
        self.type = 'variable'
        self.val = val


class Number:
    def __init__(self, val):
        self.type = 'number'
        self.val = val


class Operation:
    def __init__(self):
        self.type = 'operation'
        self.operator = None
        self.left_exp = None
        self.right_exp = None

    def set_operator(self, op):
        self.operator = op

    def set_left(self, exp):
        self.left_exp = exp

    def set_right(self, exp):
        self.right_exp = exp


class Condition:
    def __init__(self):
        self.type = 'condition'
        self.comparator = None
        self.left_exp = None
        self.right_exp = None

    def set_comparator(self, c):
        self.comparator = c

    def set_left(self, l):
        self.left_exp = l

    def set_right(self, r):
        self.right_exp = r


class IfStatement:
    def __init__(self, i):
        self.indent = i
        self.type = 'if'
        self.condition = None

    def set_condition(self, cond):
        self.condition = cond


class ElifStatement:
    def __init__(self, i):
        self.indent = i
        self.type = 'elif'
        self.condition = None

    def set_condition(self, cond):
        self.condition = cond


class ElseStatement:
    def __init__(self, i):
        self.indent = i
        self.type = 'else'


class Loop:
    def __init__(self, i):
        self.indent = i
        self.type = 'loop'
        self.condition = None

    def set_condition(self, c):
        self.condition = c


class Delimiter:
    def __init__(self, spec, indents):
        self.type = 'delimiter'
        self.specific = spec
        self.indents = indents

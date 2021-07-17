"""
========================================================================================================
* [containers.py]: This file contains the class definitions storing the parsed block data into compact *
*                  containers for allowing easy file writing across different source code types.       *
========================================================================================================
"""

"""
=========================
--   Container Types   --
=========================
* Number
* Variable
* Condition
* Assignment Operation
* Arithmetic Operator
* If/Elif/Else Structure
* Loop Structure
=========================
"""


class Number:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, variable):
        self.variable = variable


class Operator:
    def __init__(self, operator):
        self.operator = operator


class Expression:
    def __init__(self, expression):
        self.expression = expression


class Delimiter:
    def __init__(self, delimiter):
        self.delimiter = delimiter


class IfCondition:
    def __init__(self, expression):
        self.condition = expression


class ElifCondition:
    def __init__(self, expression):
        self.condition = expression


class Else:
    def __init__(self):
        self.condition = None


class LoopCondition:
    def __init__(self, expression):
        self.condition = expression

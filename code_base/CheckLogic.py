# Error: 'for' loop iterator neither a number block nor a variable
def forLoopCondition(condition):
    errorFlag = False
    numbers = ['1','2','3','4','5','6','7','8','9']
    if (condition not in numbers) and (condition != 'x') and (condition != 'y') and (condition != 'z'):
        errorFlag = True
    return errorFlag

# Error: check that number of 'end' and statement blocks are equal
def equalNumIfEnd(ip_data):
    equal = False
    endCounter = 0
    statementCounter = 0
    statements = ['if','for']
    for logic in ip_data:
        if logic in statements:
            statementCounter += 1
        elif logic == 'end':
            endCounter += 1
    if endCounter == statementCounter:
        equal = True
    return equal
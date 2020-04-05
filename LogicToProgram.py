from variableClass import Variable

# Function Definitions
# -----------------------------------------------------------------------------------------------------------------------

# Beep | Write call to beep function
def beep_function_call(op_file):
    op_file.write("beep();\n")

# Beep | Write beep function prototype
def beep_function_prototype(op_file):
    prototype = "void beep(); \n"
    op_file.write(prototype)

# Beep | Write beep function definition
def beep_function_definition(op_file): # Correct definition of buzzer function
    line1 = "void beep() { \n"
    line2 = "unsigned short freq = 500; \n"
    line3 = "unsigned long period = 1000000 / freq; \n"
    line4 = "while (freq--) { \n"
    line5 = "PORTD |= (1 << 4); \n"
    line6 = "variable_delay_us(period/2); \n"
    line7 = "PORTD &= !(1 << 4); \n"
    line8 = "variable_delay_us(period/2); \n"
    line9 = "} \n"
    line10 = "_delay_ms(500); \n"
    line11 = "} \n\n"
    definition = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11
    op_file.write(definition)

# Delay | Write variable delay prototype
def variable_delay_us_prototype(op_file):
    prototype =  "void variable_delay_us(int delay); \n"
    op_file.write(prototype)

# Delay | Write variable delay definition
def variable_delay_us_definition(op_file):
    line1 = "void variable_delay_us(int delay) {\n"
    line2 = "int i = (delay + 5) / 10; \n"
    line3 = "while (i--) {\n"
    line4 = "_delay_us(10); \n"
    line5 = "} \n"
    line6 = "} \n\n"
    definition = line1 + line2 + line3 + line4 + line5 + line6
    op_file.write(definition)




# Beep | Read the logic file and store the data in a list
def read_file(ip_filename):
    f = open(ip_filename, "r")
    line = f.readlines()
    line_b = line[0].split('\n')
    line_c = line_b[0]
    ip_data = line_c.split(',')
    return ip_data

# Syntax for print statement
# def write_print(op_file, ip_data, variables, i):
#     operators = ['+', '-', '*', '%', '/', '==', '=', '!=', '>', '<']
#     line1 = "printf(\""
#     while ip_data[i] != "end":
#         if ip_data[i] == "alex":
#             line1 += "Alex "
#             i += 1 
#         elif ip_data[i].isdigit():
#             i = write_digit(op_file, ip_data, i)
#         elif ip_data[i] in operators:
#             i = write_operator(op_file, ip_data, i)
#         elif ip_data[i] == 'x':
#
#
#     line1 += ");\n"
#     op_file.write(line1)

# End delimiter for functions and loops
def write_endStatement(op_file):
    op_file.write("} \n")

# Write newline
def write_jump(op_file):
    op_file.write(";\n")

# Write condition delimiter
def write_endCondition(op_file):
    op_file.write(") { \n")

# Write the syntax of iterative loop - for(i = 0; i<3; i++) { (followed by a newline)
def write_iterative_loop(loop_condition, op_file):
    iterativeLoop = "for(int i = 0; i < " + str(loop_condition) + "; i++) { \n"
    op_file.write(iterativeLoop)

# Check which type of loop it is
def write_loop(loop_condition, op_file):
    write_iterative_loop(loop_condition, op_file)

# if(var condition){ do something }
def write_if(op_file):
    if_statement = "if("
    op_file.write(if_statement)

# Write elif statement
def write_elif(op_file):
    elif_statement = "}\nelif{ \n"
    op_file.write(elif_statement)

# Write else statement
def write_else(op_file):
    else_statement = "}\nelse { \n"
    op_file.write(else_statement)

# formats numeric values
def write_digit(op_file, ip_data, i):
    number = ""
    number += ip_data[i]
    j = i + 1
    while ip_data[j].isdigit():
        number += ip_data[j]
        j += 1
    op_file.write(number)
    i = j
    return i

# formats operators
def write_operator(op_file, ip_data, i):
    op_file.write(ip_data[i])
    return i + 1

# Write the program inside main
def write_program(ip_data, op_file):
    functionFlags = {"beep":0} # Intended for functions not a part of the standard i/o library
    operators = ['+', '-', '*', '%', '/', '==', '=', '!=', '>', '<']

    # setup program variables
    variables = []
    xVar = Variable(ip_data, 'x') # Create 'x' variable object
    xVar.setDataTypeFlags()
    variables.append(xVar)


    i = 0
    scan_count = 0
    line1 = "int main() {\n"
    line2 = "DDRD |= (1<<4);\n"
    line3 = "return 0;\n} \n\n"
    while scan_count < 2:   # First iteration: checks for functions, second iteration: interprets and writes program
        if scan_count  == 0:
            j = 0
            while j < len(ip_data):
                if ip_data[j] == "beep":
                    beep_function_prototype(op_file)
                    variable_delay_us_prototype(op_file)
                    functionFlags["beep"] = 1
                j += 1
            scan_count += 1
            op_file.write('\n')
            op_file.write(line1)
            op_file.write(line2)
        else:
            while i < len(ip_data):
                if ip_data[i].isdigit():
                    i = write_digit(op_file, ip_data, i)
                elif ip_data[i] in operators:
                    i = write_operator(op_file, ip_data, i)
                elif ip_data[i].lower() == "loop":
                    if ip_data[i+1].isdigit():
                        j = i+1
                        loop_condition = ""
                        while ip_data[j].isdigit():
                            loop_condition += ip_data[j]
                        write_loop(loop_condition, op_file)
                        i = j
                    else:
                        write_loop(ip_data[i+1], op_file)
                        i += 2
                elif ip_data[i].lower() == "if":
                    write_if(op_file)
                    i += 1
                elif ip_data[i].lower() == "elif":
                    write_elif(op_file)
                    i += 1
                elif ip_data[i].lower() == "else":
                    write_else(op_file)
                    i += 1
                elif ip_data[i].lower() == "end":
                    write_endStatement(op_file)
                    i += 1
                elif ip_data[i].lower() == "endcon":
                    write_endCondition(op_file)
                    i += 1
                elif ip_data[i].lower() == "jump":
                    write_jump(op_file)
                    i += 1
                elif ip_data[i].lower() == "beep":
                    beep_function_call(op_file)
                    i += 1
                elif ip_data[i].lower() == 'x':
                    flag = xVar.getFlag(i)
                    if flag == 0:
                        op_file.write('x')
                    else:
                        op_file.write('int x')
                    i += 1
            scan_count += 1
    op_file.write(line3)
    return functionFlags

# Write the main body of the program
def write_main_program(ip_data, op_file):
    line1 = "#include <stdio.h> \n"
    line2 = '#include <avr/io.h> \n'
    line3 = '#include <util/delay.h> \n'
    headers = line1 + line2 + line3
    op_file.write(headers)
    functionFlags = write_program(ip_data, op_file)
    for function in functionFlags:
        if functionFlags[function] == 1:
            if function == "beep":
                beep_function_definition(op_file)
                variable_delay_us_definition(op_file)
# -----------------------------------------------------------------------------------------------------------------------

# Code for testing funtions:
def main():
    ip_filename = "blocklogic.csv"
    op_filename = "output.c"
    op_file = open(op_filename, 'w')
    ip_data = read_file(ip_filename)
    write_main_program(ip_data, op_file)
    op_file.close()
main()

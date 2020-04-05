from variableClass import Variable

# no longer make it so that variable values are remembered

# Read the logic file and store the data in a list
def read_file(ip_filename):
    f = open(ip_filename, "r")
    line = f.readlines()
    line_b = line[0].split('\n')
    line_c = line_b[0]
    ip_data = line_c.split(',')
    return ip_data

def data_size(ip_data):
    count = 0
    for i in ip_data:
        count += 1
    return count

def voice_value(variable_name, variable_value):


def write_program(ip_data, variable_values):
    size = data_size(ip_data)
    if size == 1:
        if ip_data[0] != 'x' and ip_data[0] != 'y':
            print("Error")
            return
        else:
            # make a global variable that stores the value of x
            # use speaker to output value of variable - speaker function
            if ip_data[0] == 'x':
                variable = 'x'
                value = variable_values['x']
                voice_value(variable, value)
    else:
        # stuff
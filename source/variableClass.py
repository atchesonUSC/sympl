class Variable:

    def __init__(self, ip_data, variable):
        self.data = ip_data
        self.var = variable
        self.dataTypeFlags = []

    def setDataTypeFlags(self): # Examines each occurence of specific variable and determines if new delcaration is needed
        # ifFlag = False
        # elifFlag = False
        # elseFlag = False
        # loopFlag = False
        global_flag = False
        local_flag = False
        endcon_flag = False

        i = 0
        while i < len(self.data):
            if self.data[i] == self.var:
                if (endcon_flag == False) and (global_flag == False):
                    global_flag = True
                    self.dataTypeFlags.append(1)
                elif (endcon_flag == True) and (global_flag == False) and (local_flag == False):
                    local_flag = True
                    self.dataTypeFlags.append(1)
                else:
                    self.dataTypeFlags.append(0)
            elif self.data[i] == 'end' or self.data[i] == 'elif' or self.data[i] == 'else':
                endcon_flag = False
                self.dataTypeFlags.append(0)
            elif self.data[i] == 'endcon':
                endcon_flag = True
                local_flag = False
                self.dataTypeFlags.append(0)
            else:
                self.dataTypeFlags.append(0)
            i += 1

    def getFlag(self, index):
        return self.dataTypeFlags[index]

    def getName(self):
        return self.var

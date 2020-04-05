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
        globalFlag = False
        localFlag = False
        endconFlag = False
        len_data = len(self.data)
        i = 0
        while i < len_data:
            if self.data[i] == self.var:
                if (endconFlag == False) and (globalFlag == False):
                    globalXFlag = True
                    self.dataTypeFlags.append(1)
                elif (endconFlag == True) and (globalFlag == False) and (localFlag == False):
                    localXFlag = True
                    self.dataTypeFlags.append(1)
                else:
                    self.dataTypeFlags.append(0)
            elif self.data[i] == 'end' or self.data[i] == 'elif' or self.data[i] == 'else':
                endconFlag = False
                self.dataTypeFlags.append(0)
            elif self.data[i] == 'endcon':
                endconFlag = True
                localXFlag = False
                self.dataTypeFlags.append(0)
            else:
                self.dataTypeFlags.append(0)
            i += 1

    def getFlag(self, index):
        return self.dataTypeFlags[index]

import csv

# Function Definitions:
# -----------------------------------------------------------------------------------------------------------------------

# Examines serial port, collects voltage value, appends value to corresponding block data set
def addToBlockData(blocks, iteration, blockDictionary, data):
    block = iteration % blocks
    if block == 0:
        blockDictionary["block0"].append(data)
    elif block == 1:
        blockDictionary["block1"].append(data)
    elif block == 2:
        blockDictionary["block2"].append(data)
    elif block == 3:
        blockDictionary["block3"].append(data)
    elif block == 4:
        blockDictionary["block4"].append(data)
    elif block == 5:
        blockDictionary["block5"].append(data)
    elif block == 6:
        blockDictionary["block6"].append(data)
    elif block == 7:
        blockDictionary["block7"].append(data)
    elif block == 8:
        blockDictionary["block8"].append(data)
    elif block == 9:
        blockDictionary["block9"].append(data)
    elif block == 10:
        blockDictionary["block10"].append(data)
    elif block == 11:
        blockDictionary["block11"].append(data)
    elif block == 12:
        blockDictionary["block12"].append(data)
    elif block == 13:
        blockDictionary["block13"].append(data)
    elif block == 14:
        blockDictionary["block14"].append(data)
    elif block == 15:
        blockDictionary["block15"].append(data)

# Sorts block data sets
def sortData(blockData, samples):
    for list in blockData:
        refStart = 1
        for ref in range(0, samples - 1):
            for comp in range(refStart, samples):
                if blockData[list][ref] > blockData[list][comp]:
                    temp = blockData[list][ref]
                    blockData[list][ref] = blockData[list][comp]
                    blockData[list][comp] = temp
            refStart += 1

# Reads data from serial port
def getData(serialObject):
    tryFlag = True
    num = serialObject.readline()
    while tryFlag == True:
        try:
            num = int(num)
            if (num > 1023) and (num != 2000) and (num != 3000):
                raise ValueError
        except ValueError:
            num = serialObject.readline()
        else:
            tryFlag = False
    return num

# Prints ordered block data sets
# ** Not important function, just for debugging
def printData(blockData, block):
    if block == 0:
        print("block0:")
        for num in blockData["block0"]:
            print(num)
    elif block == 1:
        print("block1:")
        for num in blockData["block1"]:
            print(num)
    elif block == 2:
        print("block2:")
        for num in blockData["block2"]:
            print(num)
    elif block == 3:
        print("block3:")
        for num in blockData["block3"]:
            print(num)
    elif block == 4:
        print("block4:")
        for num in blockData["block4"]:
            print(num)
    elif block == 5:
        print("block5:")
        for num in blockData["block5"]:
            print(num)
    elif block == 6:
        print("block6:")
        for num in blockData["block6"]:
            print(num)
    elif block == 7:
        print("block7:")
        for num in blockData["block7"]:
            print(num)
    elif block == 8:
        print("block8:")
        for num in blockData["block8"]:
            print(num)
    elif block == 9:
        print("block9:")
        for num in blockData["block9"]:
            print(num)
    elif block == 10:
        print("block10:")
        for num in blockData["block10"]:
            print(num)
    elif block == 11:
        print("block11:")
        for num in blockData["block11"]:
            print(num)
    elif block == 12:
        print("block12:")
        for num in blockData["block12"]:
            print(num)
    elif block == 13:
        print("block13:")
        for num in blockData["block13"]:
            print(num)
    elif block == 14:
        print("block14:")
        for num in blockData["block14"]:
            print(num)
    elif block == 15:
        print("block15:")
        for num in blockData["block15"]:
            print(num)

# Find median of sample values for each block
def findMedian(blockDict, samples, medianValues):
    medianIndex = int((samples + 1) / 2)
    for list in blockDict:
        medianValues.append(blockDict[list][medianIndex])

# checks if blocks have been placed on the board
def checkForBlocks(medianList):
    blockExists = False
    for val in medianList:
        if val != 1023:
            blockExists = True
            return blockExists
    return blockExists

# if blocks on board, grabs index of first block occurrence
def firstBlockIndex(medianList, numBlocks):
    index = None
    counter = 0
    while counter < numBlocks:
        if medianList[counter] != 1023:
            index = counter
            break
        counter += 1
    return index

# if blocks on board, grabs index of last block occurrence
def lastBlockIndex(medianList, numBlocks):
    index = None
    counter = numBlocks-1
    while counter != -1:
        if medianList[counter] != 1023:
            index = counter
            break
        counter -= 1
    return index

# Error check for block spacing - first block can be anywhere
# but no spaces between blocks
# Key: -1 == no blocks, 0 == no error, 1 == error
def spacingError(medianList, numBlocks):
    error = 0
    blocksExist = checkForBlocks(medianList)
    if blocksExist == True:
        firstBlock = firstBlockIndex(medianList, numBlocks)
        lastBlock = lastBlockIndex(medianList, numBlocks)
        if firstBlock == lastBlock:
            error = 0
            return error
        else:
            counter = firstBlock
            while counter < numBlocks:
                if counter == firstBlock:
                    if medianList[counter+1] == 1023:
                        error = 1
                        return error
                elif counter == lastBlock:
                    if medianList[counter-1] == 1023:
                        error = 1
                        return error
                else:
                    if (medianList[counter] != 1023) and (medianList[counter-1] != 1023) and (medianList[counter+1] != 1023):
                        error = 0
                    else:
                        error = 1
                        return error
            return error
    else:
        error = -1
        return error

# Print median values
# ** not important, meant for debuggin
def printResistance(medianValues):
    print("Resistance Values:")
    for val in medianValues:
        print(val)

# Reads serial port, appends value to corresponding block dataset
def readSerialAddToDataset(ser, blocks, iteration, blockData):
    data = getData(ser)
    addToBlockData(blocks, iteration, blockData, data)

# Convert analog values to voltage(V), then find resistance of block
def calculateBlockResistance(medianList, vin, boardResistance, blocks):
    conversionFactor = vin / 1023
    for index in range(0, blocks):
        medianList[index] *= conversionFactor
        medianList[index] = (medianList[index] * boardResistance) / (vin - min(medianList[index],4.9))

# Clear all data values from block data sets
def clearBlockData(blockData):
    for key in blockData:
        blockData[key] = []

# Read csv file containing block mapping
def createBlockMapping(fileName, dict):
    with open(fileName, 'r') as blockMappingFile:
        file_reader = csv.reader(blockMappingFile)
        next(file_reader)
        for line in file_reader:
            dict[line[0]] = float(line[1])

# Create error buffer for each block type - utilizes error equation
def resistorError(fileName, dict, boardResistance):
    createBlockMapping(fileName, dict)
    for key in dict:
        coeff = 6
        numerator = coeff*pow(dict[key], 2) + (boardResistance*coeff*2)*dict[key] + coeff*pow(boardResistance, 2)
        denominator = 1017*boardResistance - coeff*dict[key]
        error = numerator/denominator
        upperBound = dict[key]+error
        lowerBound = dict[key]-error
        dict[key] = [] # Create dictionary of error
        dict[key].append(lowerBound)
        dict[key].append(upperBound)

# Writes block logic to .csv file
def writeLogicFile(blockPseudoCode):
    with open('blocklogic.csv', 'w') as blockLogicFile:
        csvWriter = csv.writer(blockLogicFile, delimiter=',')
        csvWriter.writerow(blockPseudoCode)
# -----------------------------------------------------------------------------------------------------------------------
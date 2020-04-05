# IMPORTS!
import serial
import BlocksToLogic
import LogicToProgram
import CompileUpload


# Main Program:
#-----------------------------------------------------------------------------------------------------------------------
def main():
    mappingGuideFile = "BlockMapping.csv"    # Stores block mapping information
    blocks = 16  # Number of board block spaces
    samplesPerBlock = 20    # Number of sample measurements per block space
    vin = 5     # Voltage supplied by Arduino Mega
    boardResistance = 68000   # reference resistor size in board
    serialPort = "/dev/cu.usbmodem14101" # Port for board micro-controller input
    baudRate = 9600
    ser = serial.Serial(serialPort, baudRate)     # Creates a Serial Object - Basically a bridge between program and serial port
    blockData = {"block0":[],      # Stores sample data for each block
                 "block1":[],
                 "block2":[],
                 "block3":[],
                 "block4":[],
                 "block5":[],
                 "block6":[],
                 "block7":[],
                 "block8":[],
                 "block9":[],
                 "block10":[],
                 "block11":[],
                 "block12":[],
                 "block13":[],
                 "block14":[],
                 "block15":[]}
    blockMedianList = []    # stores median value of data set for each block space
    blockPseudoCode = []    # stores logic to be written to .csv file
    blockMappingRange = {}   # stores block mapping ranges for pseudo-code

    while 1:    # main program loop

        while BlocksToLogic.getData(ser) != 3000: # Waits until the start flag is raised
            pass
        outerCounter = 0  # Controls number of sets of data are collected (e.g. data for each block = 1 set of data)
        while outerCounter < samplesPerBlock:
            iteration = 0
            data = BlocksToLogic.getData(ser)
            while data != 2000: # Waits until start flag for block sequence has been received
                data = BlocksToLogic.getData(ser)
            while 1:    # collects single set of block sequence data
                if iteration == blocks:
                    break
                else:
                    BlocksToLogic.readSerialAddToDataset(ser, blocks, iteration, blockData)
                    iteration += 1
            outerCounter +=1

        # Upload mapping data from .csv file and get resistor error range
        BlocksToLogic.sortData(blockData, samplesPerBlock)  # Sort block analog data
        BlocksToLogic.findMedian(blockData, samplesPerBlock, blockMedianList) # Find median value from each set of block data

        # Conduct error inspection for block placement
        placementError = BlocksToLogic.spacingError(blockMedianList, blocks)

        if placementError == 1:
            BlocksToLogic.clearBlockData(blockData)
            blockMedianList = []
            print("Uh-oh! It appears there's an error in your code!")
        elif placementError == -1:
            BlocksToLogic.clearBlockData(blockData)
            blockMedianList = []
            print("Please make sure blocks are connected to the board!")
        else:
            BlocksToLogic.calculateBlockResistance(blockMedianList, vin, boardResistance, blocks)  # Convert analog value to resistance (Ohms)
            BlocksToLogic.resistorError(mappingGuideFile, blockMappingRange, boardResistance)

            # Check each block in blockMedianList and find the range that it belongs to in the blockMapping dictionary
            for block in blockMedianList:
                # print(block)
                for blockType in blockMappingRange:
                    if (block >= blockMappingRange[blockType][0]) and (block <= blockMappingRange[blockType][1]): # checks upper and lower bound of error range
                        blockPseudoCode.append(blockType)
                    # if blockMappingRange[blockType][0] > 0:
                    #     print(blockMappingRange[blockType][0])
                    #     print(blockMappingRange[blockType][1])

            # Write blockPseudoCode to .csv file
            BlocksToLogic.writeLogicFile(blockPseudoCode)

            # Read .csv of pseudo-code and write .c file
            ip_filename = "blocklogic.csv"
            op_filename = "output.c"    # name of created .c file that gets uploaded to external micro-controller
            op_file = open(op_filename,'w')
            ip_data = LogicToProgram.read_file(ip_filename)

            # Conduct error inspection for logic
            # ** Code here **

            # Creates .c file representation of block data
            LogicToProgram.write_main_program(ip_data, op_file)
            op_file.close()

            # Clear block data
            BlocksToLogic.clearBlockData(blockData)
            blockMedianList = []
            blockMappingRange = {}
            blockPseudoCode = []

            # Upload program to Arduino chip
            CompileUpload.compileAndUpload()
# -----------------------------------------------------------------------------------------------------------------------
main()

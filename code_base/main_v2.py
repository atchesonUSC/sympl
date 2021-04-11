import pin_config
# import RPi.GPIO as GPIO
from ParseTool import ParseTool
# from RfidArray import RfidArray

"""
========================================================================================================
* [main_v2.py.py]: Executes main function for reading each block space, and then converting that block *
*            information into executable code (can choose C or Python formatting of resulting program) *
========================================================================================================
"""

"""
==================================================================
* [SECTION] Select option for parsing to C or Python source code *
==================================================================
"""

"""
# Specify source file language...
src_code_format = input('[STATUS] Source options: Python (\'p\'), C (\'c\'): ')
while src_code_format.lower() != 'p' and src_code_format.lower() != 'c':
    src_code_format = input('[STATUS] Source options: Python (\'p\'), C (\'c\'): ')
"""

"""
===================================================================
* [SECTION] Create output file for storing executable source code *
===================================================================
"""

# Create file for writing...
# ofile_name = input('[STATUS] Enter name for source code file: ')
ofile = open('output.py', 'w')

"""
==========================================
* [SECTION] Configure input/ output pins *
==========================================
"""
"""
# Configure RPi.GPIO mode...
GPIO.setmode(GPIO.BOARD)

# Configure external device pins...
GPIO.setup(pin_config.SPEAKER, GPIO.OUT)
GPIO.setup(pin_config.BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""
"""
==============================================================
* [SECTION] Read block program from tactile programming tool *
==============================================================
"""

# Array of RFID readers
'''
num_readers = 16
rfid_readers = RfidArray(num_readers)
'''

count = 0
while count == 0:
    count += 1

    """
    # Wait for Start Button to be pressed...
    while GPIO.input(pin_config.BUTTON) == GPIO.HIGH:
        pass

    # Read block code...
    block_code = rfid_readers.read()
    """

    block_code = ['x', '=', '3', 'end', 'if', 'x', '>', '5', 'end', 'x', '=', 'x', '+', '9', 'end', 'end-conditional']

    """
    ==============================================
    * [SECTION] Parse block code into containers *
    ==============================================
    """

    # Parse block code to source code...
    src_lines_processed = ParseTool(block_code).parse()

    """
    ===============================================
    * [SECTION] Write parsed code to source file *
    ===============================================
    """

    for src_line in src_lines_processed:
        ofile.write(src_line + '\n')

    """
    =================================
    * [SECTION] Execute output file *
    =================================
    """

import os
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

print('===============================================')
print('* HaRVI Lab Software - Tangible Coding Language')
print('* Developer: Alex Atcheson')
print('* Email: saatcheson@gmail.com')
print('===============================================\n')

"""
==================================================================
* [SECTION] Select option for parsing to C or Python source code *
==================================================================
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

# Open output.py file for writing translated Python code
output_file = 'output.py'
ofile = open(output_file, 'w')

"""
==========================================
* [SECTION] Configure input/ output pins *
==========================================
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
num_readers = 24
rfid_readers = RfidArray(num_readers)
'''

parser = ParseTool()

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

    block_code1 = ['x', '=', '3', 'end', 'if', 'x', '>', '5', 'end', 'x', '=', 'x', '+', '9', 'end', 'end-conditional']
    block_code2 = ['x', '=', '3', 'end']
    block_code3 = ['loop', '5', 'end', 'x', '=', '4', 'end', 'y', '=', '9', 'end', 'end-loop']
    block_code4 = ['x', '=', '7', 'if', 'x', '<', '3', 'end', 'x', '=', '5', 'end', 'elif', 'x', '<', '1', 'end', 'x', '=', '3', 'end', 'end-conditional-structure']
    block_code5 = ['beep', 'end']
    test = block_code5

    """
    ==============================
    * [SECTION] Parse block code *
    ==============================
    """
    # Parse block code to source code
    parser.parse(test)

    # check if any parser errors encountered
    if parser.found_error():
        parser.reset_error()
    else:
        src_lines_processed = parser.format_srclines()

        """
        =======================================================
        * [SECTION] Write formatted source code lines to file *
        =======================================================
        """
        ofile.write('import speaker\n\n')
        ofile.write('# audio and text\n')
        ofile.write('txt = \'beep\'\n')
        ofile.write('audio = speaker.Speaker()\n\n')

        for src_line in src_lines_processed:
            ofile.write(src_line + '\n')
        print('[STATUS] Success! Output file written')

        """
        =================================
        * [SECTION] Execute output file *
        =================================
        interpreter = 'python3'
        output_file_path = '~/sympl/source/output.py'
        os.system(interpreter + ' ' + output_file_path)
        """

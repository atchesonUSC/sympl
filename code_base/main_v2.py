"""
========================================================================================================
* [main_v2.py.py]: Executes main function for reading each block space, and then converting that block *
*            information into executable code (can choose C or Python formatting of resulting program) *
========================================================================================================
"""


import parser


"""
==============================================================
* [SECTION] Read block program from tactile programming tool *
==============================================================
"""


"""
==================================================================
* [SECTION] Select option for parsing to C or Python source code *
==================================================================
"""

# specify in which language we want the source file to be written
src_code_format = input('[STATUS] Source options: Python (\'p\'), C (\'c\'): ')
while src_code_format.lower() != 'p' and src_code_format.lower() != 'c':
    src_code_format = input('[STATUS] Source options: Python (\'p\'), C (\'c\'): ')

"""
===================================================================
* [SECTION] Create output file for storing executable source code *
===================================================================
"""

# choose file name for storing translated source code
ofile_name = input('[STATUS] Enter name for source code file: ')

# create file (if it doesn't exist)
ofile = open(ofile_name, 'w')

"""
==============================================
* [SECTION] Parse block code into containers *
==============================================
"""


"""
==================================================
* [SECTION] Write containers data to source file *
==================================================
"""


"""
=================================
* [SECTION] Execute output file *
=================================
"""

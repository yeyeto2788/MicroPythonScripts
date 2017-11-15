# This file is executed on every boot (including wake-boot from deepsleep)
"""
IMPORT MODULES NEEDED
"""
import gc
import os


"""
DECLARE FUNCTIONS
"""

def CheckMSG_File():
    """
    Check the file lines, if the line number is above 10 it will overwrite the file empty
    
    Returns:
            Nothing.
    """
    Files = os.listdir()
    MSG_file = 'messages.txt'
    with open(MSG_file,'r') as f:
        Data = f.readlines()
        DataLenght = len(Data)
        f.close()
    if DataLenght > 10:
        with open(MSG_file,'w') as f:
            f.close()


"""
EXECUTE THE CODE
"""
gc.collect()
CheckMSG_File()

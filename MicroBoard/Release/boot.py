import gc
import os

def CheckMSG_File():
    Files = os.listdir()
    MSG_file = 'messages.txt'
    with open(MSG_file,'r') as f:
        Data = f.readlines()
        DataLenght = len(Data)
        f.close()
    if DataLenght > 10:
        with open(MSG_file,'w') as f:
            f.close()

gc.collect()
CheckMSG_File()

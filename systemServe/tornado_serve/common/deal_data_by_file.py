import os

dirpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
filepath=dirpath+'/systemServe.conf'

def getDictDataFromFile():
    with open(filepath,'r') as f:
        systemSet=f.read()
        systemSet=eval(systemSet)
    return systemSet

def setDataInFile(systemSet):
    with open(filepath,'w') as f:
        f.write(systemSet)
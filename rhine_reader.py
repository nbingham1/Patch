from rhine import *

def rhineGenerate(keyfile):
    rhines = []
    f = open(keyfile)
    for el in f:
        rhines.append(Rhine(el))
    return rhines



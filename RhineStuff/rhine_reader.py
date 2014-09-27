from rhine import *

#class 

def rhineGenerate(keyfile):
    rhines = []
    f = open(keyfile)
    for el in f:
        rhines.append(Rhine(el))
    return rhines



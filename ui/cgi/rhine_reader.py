from rhine import *
import time

class RhineBundle:
    rhines = []
    lastRhine = 0
    timeouts = 0
    def rhineGenerate(self, keyfile):
        f = open(keyfile)
        for el in f:
            self.rhines.append(Rhine(el))
    
    def freshRhine(self):
        #time.sleep(.5)
        self.lastRhine = (self.lastRhine + 1)%len(self.rhines)
        return self.rhines[self.lastRhine]
    

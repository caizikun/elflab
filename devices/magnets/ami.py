""" AMI Magnet Power Supplies """
import visa
import time
from .magnet_base import MagnetBase

class Model420(MagnetBase):
    def __init__(self, address):
        self.address = address
        
        self.connected = False
        self.H = float('nan')
        self.I = float('nan')
        
    def connect(self):
        rm = visa.ResourceManager()
        self.gpib = rm.open_resource("GPIB::{:n}".format(self.address))
        self.gpib.write("CONFigure:FIELD:UNITS 1")  # Configure the field unit to Tesla
        print("        AMI Model 420 magnet programmer connected, GPIB={:n}.".format(self.address))        
        self.connected = True
    
    def read(self): # returns (t, H/Tesla, I_magnet/A)
        stat = str(self.gpib.query("CURRent:MAGnet?"))
        self.I = float(stat)
        stat = str(self.gpib.query("FIELD:MAGnet?"))
        self.H = float(stat)
            
        return (time.perf_counter(), self.H, self.I)
        

        
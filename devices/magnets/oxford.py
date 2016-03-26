""" Oxford Magnet Power Supplies """
import visa
import time
from .magnet_base import MagnetBase

class IPS120_10(MagnetBase):
    def __init__(self, address):
        self.address = address
        
        self.connected = False
        self.H = float('nan')
        self.I = float('nan')
        
    def connect(self):
        rm = visa.ResourceManager()
        self.gpib = rm.open_resource("GPIB::{:n}".format(self.address), read_termination='\r', write_termination='\r')
        print("        Oxford IPS 120-10 magnet power supply connected, GPIB={:n}.".format(self.address))        
        self.connected = True
    
    def read(self): # returns (t, H/Tesla, I_magnet/A)
        stat = str(self.gpib.query("X"))
        while len(stat) != 15:
            stat = str(self.gpib.query("X"))
        
        if (stat[8] == '0') or (stat[8] == '2'):    # persistent switch closed
            # use persistent values
            err = True  # error flag for detecting GPIB error
            while err:
                try:
                    s = str(self.gpib.query("R18")).strip("Rr")
                    self.H = float(s)
                except:
                    pass
                else:
                    err = False
            err = True  # error flag for detecting GPIB error
            while err:
                try:
                    s = str(self.gpib.query("R16")).strip("Rr")
                    self.I = float(s)
                except:
                    pass
                else:
                    err = False
        else:   # persistent switch open or not present
            # use demand / measured values
            err = True  # error flag for detecting GPIB error
            while err:
                try:
                    s = str(self.gpib.query("R7")).strip("Rr")  # Demand field
                    self.H = float(s)
                except:
                    pass
                else:
                    err = False
            err = True  # error flag for detecting GPIB error
            while err:
                try:
                    s = str(self.gpib.query("R2")).strip("Rr")  # Measured Current
                    self.I = float(s)
                except:
                    pass
                else:
                    err = False
            
        return (time.perf_counter(), self.H, self.I)
        

        
import pyvisa as visa
import time

class Eload_2380(object):

    def __init__(self, address: str):
        self._ip = address.strip()
        print("self_ip",self._ip)
        # Get the Load Model
        if self._ip != "":
            rm = visa.ResourceManager()
            print("address:", self._ip)
            self.load = rm.open_resource(self._ip, read_termination='\n')
            self.load.timeout = 20000
            self.load.write_termination = '\n'
            self.load.read_termination = '\n'
        else:
            print("Declaring no load present. Not setting up")
            self.load = 0

    def getIdn(self):
        '''
        The Identification (IDN) Queries outputs an identifying string.
        The response will show the following information:<manufacturer's name>, <model number>, <not used-always 0>, <revision number>

        :parameter  : None
        :returns    : dict
        '''
        cmd = '*IDN?'
        return {'Idn': self.load.query(cmd)}


    def set_current(self, current, range):
        self.load.write(f'CURR')
        self.load.write(f'CURR:RANG {range}')
        print(f'CURRENT RANGE SET TO {range} A')
        self.load.write(':CURR ' + current + ' ,')


    def EL_CH_OFF(self):
        self.load.write('OUTP OFF')
        result = self.load.query('OUTP?')


    def EL_CH_ON(self):
        self.load.write('OUTP ON')
        result = self.load.query('OUTP?')



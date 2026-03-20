import pyvisa as visa
import time

class DMM_6500(object):

    def __init__(self, address: str):
        self._ip = address.strip()
        print("self_ip",self._ip)
        # Get the Load Model
        if self._ip != "":
            rm = visa.ResourceManager()
            print("address:", self._ip)
            self.dmm = rm.open_resource(self._ip, read_termination='\n')
            self.dmm.timeout = 20000
            self.dmm.write_termination = '\n'
            self.dmm.read_termination = '\n'
        else:
            print("Declaring no dmm present. Not setting up")
            self.dmm = 0

    def getIdn(self):
        '''
        The Identification (IDN) Queries outputs an identifying string.
        The response will show the following information:<manufacturer's name>, <model number>, <not used-always 0>, <revision number>

        :parameter  : None
        :returns    : dict
        '''
        cmd = '*IDN?'
        return {'Idn': self.dmm.query(cmd)}

    def measVolt(self):
        ret = self.dmm.query('MEAS:VOLT:DC?')
        return ret

    def measCurrent(self):
        ret = float(self.dmm.query('MEAS:CURR:DC?'))
        return ret



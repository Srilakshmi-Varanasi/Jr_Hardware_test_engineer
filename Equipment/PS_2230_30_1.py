import pyvisa as visa
import time

class PS_2230_30_1(object):

    def __init__(self, address: str):
        self._ip = address.strip()
        print("self_ip",self._ip)
        # Get the PSU Model
        if self._ip != "":
            rm = visa.ResourceManager()
            print("address:", self._ip)
            self.psu = rm.open_resource(self._ip, read_termination='\n')
            self.psu.timeout = 20000
            self.psu.write_termination = '\n'
            self.psu.read_termination = '\n'
        else:
            print("Declaring no PSU present. Not setting up")
            self.psu = 0


    def getIdn(self):
        '''
        The Identification (IDN) Queries outputs an identifying string.
        The response will show the following information:<manufacturer's name>, <model number>, <not used-always 0>, <revision number>

        :parameter  : None
        :returns    : dict
        '''
        cmd = '*IDN?'
        return {'Idn': self.psu.query(cmd)}


    def PWR_CH_SET(self,channel, v, i):
            self.psu.write('INST CH' + channel)
            self.psu.write('APPL' + ' CH' + channel + ', ' + v + ', ' + i)
            # self.psu.write("VOLT"+" "+v)
            # self.psu.write("CURR"+" "+i)
            print('Channel', channel, '\n---------------\n')
            print(v + 'V')
            print(i + 'A')

    def channel_ON(self,channel):
            self.psu.write('INST CH' + channel)
            self.psu.write("CHAN:OUTP 1")
            result = self.psu.query("CHAN:OUTP?")
            result = int(result)
            if result == 0:
                print('\nchannel', channel, ' turned OFF', end='')
            elif result == 1:
                print('\nchannel', channel, ' turned ON', end='')

    def channel_OFF(self,channel):
            self.psu.write('INST CH' + channel)
            self.psu.write("CHAN:OUTP 0")
            result = self.psu.query("CHAN:OUTP?")
            result = int(result)
            if result == 0:
                print('\nchannel', channel, ' turned OFF', end='')
            elif result == 1:
                print('\nchannel', channel, ' turned ON', end='')
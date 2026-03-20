import pyvisa as visa
import time

class DSOX6004A(object):

    def __init__(self, address: str):
        self._ip = address.strip()
        print("self_ip",self._ip)
        # Get the Load Model
        if self._ip != "":
            rm = visa.ResourceManager()
            print("address:", self._ip)
            self.inst = rm.open_resource(self._ip, read_termination='\n')
            self.inst.timeout = 20000
            self.inst.write_termination = '\n'
            self.inst.read_termination = '\n'
        else:
            print("Declaring no scope present. Not setting up")
            self.inst = 0

    def getIdn(self):
        '''
        The Identification (IDN) Queries outputs an identifying string.
        The response will show the following information:<manufacturer's name>, <model number>, <not used-always 0>, <revision number>

        :parameter  : None
        :returns    : dict
        '''
        cmd = '*IDN?'
        return {'Idn': self.inst.query(cmd)}


    def saveScreen(self, fName='RISETIME'):
        print("saveScreen")
        from datetime import datetime
        fName = str(fName)
            # self.fName = fName
            #time.sleep(4)
        print("After sleep")
        imgData = self.genReadBin(':DISPlay:DATA? PNG')
        print("After img data")
        imgRdata = bytes(imgData)
        ImgName = (fr"C:\{fName}_" + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.png')
        print("before open image")
        with open(ImgName, 'wb') as f:
            f.write(imgRdata)
        print("before")
        return ImgName

    def clear_display(self):
        self.inst.write(":DISPlay:CLEar")

    def get_meas_vmin(self, source):
        ret = self.inst.query(":MEASure:VMIN? {}".format(source))
        return float(ret)

    def get_meas_vavg(self, mode, source):
        """
        :param mode: {CYCLe | DISPlay}
        :param source: {CHANnel<N> | DIFF<D> | COMMonmode<C> | FUNCtion<F> | WMEMory<R> |
                    CLOCk | MTRend | MSPectrum | EQUalized<L> | XT<X> | INPut | CORRected |
                    ERRor | LFPR | NREDuced}
        """
        ret = self.inst.query(":MEASure:VAVerage? {},{}".format(mode, source))
        return ret

    def get_meas_vmax(self, source):
        ret=self.inst.query(":MEASure:VMAX? {}".format(source))
        return float(ret)

    def set_recall_setup(self,fname):
        self.inst.write(":RECall:SETup '{}'".format(fname))

    def get_x_delta(self):
        return self.inst.query("MARK:XDEL?")

    def get_y_delta(self):
        return self.inst.query("MARK:YDEL?")

    def set_single(self):
        self.inst.write(":SINGLE")
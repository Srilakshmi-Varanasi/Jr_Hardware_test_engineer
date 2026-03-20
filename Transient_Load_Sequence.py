'''
Trasient load test execution flow :
perfrom trasient load testcase across
voltages : ["3.6", "1.8", "3.3", "2.5"] by applying loads : ["100mA", "300mA"] at room temperature typically 25C.
For each voltage condition apply defined loads and capture the waveform using ocilloscope and record DMM value.
Generate the CSV file with the recorded output values.
'''

# importing all required instrument drivers of equipments
from Equipment.DMM_6500 import DMM_6500
from Equipment.DSOX6004A import DSOX6004A
from Equipment.Eload_2380 import Eload_2380
from Equipment.PS_2230_30_1 import PS_2230_30_1

import time
import pandas as pd
from datetime import datetime

# creating objects to instrument drivers classes of listed equipments
# And provide the addresses of each equipment by assigning it to the address variable
dmm = DMM_6500(address="")
scope = DSOX6004A(address="")
load = Eload_2380(address="")
supply = PS_2230_30_1(address="")

time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
headers = ["Testcase_name", "Main_supply", "Input_Voltage", "Load_value", "Output_Vmin", "Output_Vavg", "Output_Vmax", "Dmm_Output"]
file_name = f"Transient_load_{time_stamp}.csv"

# Generate the Output CSV file by writing Headers
df = pd.DataFrame(columns=headers)
df.to_csv(file_name, index=False)

main = "5"
voltage_list = ["3.6", "1.8", "3.3", "2.5"]
load_list = ["100mA", "300mA"]
curr_dict = {"3.6": "1", "1.8": "0.5", "3.3": "0.5", "2.5": "0.5"}
testcase = "Transient_load"

def test_run():
    for voltage in voltage_list:
        supply.PWR_CH_SET('1', main, '2.5')
        supply.channel_ON('1')
        time.sleep(2)
        current = curr_dict[voltage]
        supply.PWR_CH_SET('2', voltage, current)
        supply.channel_ON('2')
        time.sleep(2)

        for load1 in load_list:
            load.set_current(current= load1, range="MIN")
            load.EL_CH_ON()
            time.sleep(2)

            scope.set_recall_setup("setup_0")
            time.sleep(2)
            scope.clear_display()
            time.sleep(2)
            scope.set_single()
            time.sleep(2)

            img_name = f"Transinet_Load_{voltage}V_{load1}"
            scope.saveScreen(img_name)
            time.sleep(2)
            vmax = scope.get_meas_vmax('CHANnel1')
            vmin = scope.get_meas_vmin('CHANnel1')
            vavg = scope.get_meas_vavg('DISPlay', 'CHANnel1')
            dmm_out = dmm.measVolt()

            # Append values to the CSV file
            data = {"Testcase_name": [testcase], "Main_supply": [main], "Input_Voltage": [voltage], "Load_value": [load1], "Output_Vmin": [vmin], "Output_Vavg": [vavg], "Output_Vmax": [vmax], "Dmm_Output": [dmm_out]}
            df = pd.DataFrame(data)
            df.to_csv(file_name, mode="a", header=False, index=False)

            load.EL_CH_OFF()
            time.sleep(2)

        supply.channel_OFF('2')
        time.sleep(2)
        supply.channel_OFF('1')
        time.sleep(2)

test_run()
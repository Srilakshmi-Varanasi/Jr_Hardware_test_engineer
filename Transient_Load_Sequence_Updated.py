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
eload = Eload_2380(address="")
psu = PS_2230_30_1(address="")

time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
headers = ["Rail", "Load Step(mA)", "Droop(mV)", "Recovery Time(uS)", "Overshoot (mV)", "Ringing", "Trigger(mS)"]
file_name = f"Transient_load_{time_stamp}.csv"

# Generate the Output CSV file by writing Headers
df = pd.DataFrame(columns=headers)
df.to_csv(file_name, index=False)


rails = {
    "3V3": {"volt": 3.3, "curr": 2, "l_low": 0.1, "l_high": 1.5},
    "2V5": {"volt": 2.5, "curr": 1, "l_low": 0.1, "l_high": 0.75},
    "1V8": {"volt": 1.8, "curr": 2, "l_low": 0.1, "l_high": 1.5},
    "1V35": {"volt": 1.35, "curr": 2, "l_low": 0.1, "l_high": 1.5},
    "1V_PS": {"volt": 1.0, "curr": 2, "l_low": 0.1, "l_high": 1.5},
    "1V_PL": {"volt": 1.0, "curr": 2, "l_low": 0.1, "l_high": 1.5},
    "1V1_E0": {"volt": 1.1, "curr": 1, "l_low": 0.1, "l_high": 0.5},
    "2V5_E0": {"volt": 2.5, "curr": 1, "l_low": 0.1, "l_high": 0.5}
}

def run_test():
    for rail, params in rails.items():
        print(f"\nTesting rail: {rail}")

        psu.PWR_CH_SET("1", params["volt"], params["curr"])
        psu.channel_ON("1")
        time.sleep(2)

        eload.set_current(params["l_low"], "MIN")
        eload.EL_CH_ON()
        time.sleep(2)

        scope.set_timebase("1ms")
        scope.set_probe("1", "1:1")
        scope.set_coupling("AC")

        # ===================    Positive Load Step      ==================================

        scope.set_trigger(edge="rising")
        scope.clear_display()
        time.sleep(2)
        scope.set_single()
        time.sleep(2)


        eload.step_current(
            start=params["l_low"],
            stop=params["l_high"],
            transition_time="100ns"
        )


        vmax = scope.get_meas_vmax('CHANnel1')
        vmin = scope.get_meas_vmin('CHANnel1')
        vavg = scope.get_meas_vavg('CHANnel1')
        deltax = scope.get_x_delta()
        overshoot = vmax-vavg
        v_droop = vmax-vmin
        time.sleep(2)
        img_name = f"Transinet_Load_{rail}_Positive_Load_Step_{l_low}_{l_high}_{v_droop} droop"
        scope.saveScreen(img_name)


        # Append values to the CSV file
        load_step = f"{l_low}-{l_high}"
        data = {"Rail": [rail], "Load Step(mA)": [load_step], "Droop(mV)": [v_droop], "Recovery Time(uS)": [deltax], "Overshoot (mV)": [overshoot], "Ringing": ["N"], "Trigger(mS)": [deltax]}
        df = pd.DataFrame(data)
        df.to_csv(file_name, mode="a", header=False, index=False)

        # ===================    Negative Load Step      ==================================

        scope.set_trigger(edge="falling")
        scope.clear_display()
        time.sleep(2)
        scope.set_single()
        time.sleep(2)

        eload.step_current(
            start=params["high"],
            stop=params["low"],
            transition_time="100ns"
        )


        vmax = scope.get_meas_vmax('CHANnel1')
        vmin = scope.get_meas_vmin('CHANnel1')
        vavg = scope.get_meas_vavg('DISPlay', 'CHANnel1')
        deltax = scope.get_x_delta()
        overshoot = vmax-vavg
        v_droop = vmin-vmax
        time.sleep(2)

        img_name = f"Transinet_Load_{rail}_Negative_Load_Step_{l_high}_{l_low}_{v_droop} droop"
        scope.saveScreen(img_name)


        # Append values to the CSV file
        load_step = f"{l_high}-{l_low}"
        data = {"Rail": [rail], "Load Step(mA)": [load_step], "Droop(mV)": [v_droop], "Recovery Time(uS)": [deltax], "Overshoot (mV)": [overshoot], "Ringing": ["Y"], "Trigger(mS)": [deltax]}
        df = pd.DataFrame(data)
        df.to_csv(file_name, mode="a", header=False, index=False)

        eload.EL_CH_OFF()
        time.sleep(2)

        psu.channel_OFF('1')

run_test()
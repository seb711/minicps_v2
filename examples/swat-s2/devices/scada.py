"""
swat-s1 scada.py
"""
import datetime
import time
import csv
from minicps.devices import Scada
from utils import PLC_PERIOD_SEC, SCADA_TAGS, STATE, SCADA_PROTOCOL, SCADA_VALUES
from utils import PP_PERIOD_SEC, PLC_SAMPLES
from utils import PUMP_FLOWRATE_IN
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("seaborn")

index = count()

fieldnames = ["time"] + [x["value"][0] for x in SCADA_TAGS]


# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatScada(Scada):
    def pre_loop(self, sleep=0.1):
        self.fig, self.axis_list = plt.subplots(nrows=len(fieldnames) - 1, ncols=1)

        info = {
            "time": 0,
        }

        for item in SCADA_TAGS:
            val = self.receive(item["value"], item["address"])
            if val:
                info[item["value"][0]] = float(val)
            else:
                info[item["value"][0]] = 0

        self.data = pd.DataFrame.from_records([info])

    def main_loop(self):
        """fit101 main loop.

        - reads sensors value
        - updates its enip server
        """

        def animate(i):
            info = {
                "time": next(index),
            }

            # COULD BE ASYNCHRONOUS IN THREADS
            for item in SCADA_TAGS:
                val = self.receive(item["value"], item["address"])
                if val:
                    info[item["value"][0]] = float(val)
                else:
                    info[item["value"][0]] = 0


            self.data = self.data.append(info, ignore_index=True)

            x = self.data["time"]
            for idx, axis in enumerate(self.axis_list):
                axis.cla()
                axis.plot(x, self.data[fieldnames[idx + 1]], label=fieldnames[idx + 1])
                axis.set_title(SCADA_VALUES[fieldnames[idx + 1]][0])
                axis.set_xlabel("time in milliseconds")
                axis.set_ylabel(SCADA_VALUES[fieldnames[idx + 1]][1])

            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, interval=PLC_PERIOD_SEC*1000*10)
        # plt.tight_layout()
        plt.show()


if __name__ == "__main__":

    # notice that memory init is different form disk init
    scada = SwatScada(name="scada", protocol=SCADA_PROTOCOL)

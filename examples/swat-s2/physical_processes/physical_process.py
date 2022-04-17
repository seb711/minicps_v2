import datetime
from minicps.process import Process

from utils import LIT_201_M, PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES
import time
import sys
import pandas as pd

sys.stdout.flush()

# SPHINX_SWAT_TUTORIAL TAGS(
FIT101 = ("FIT101", 3)
MV101 = ("MV101", 4)
LIT101 = ("LIT101", 5)
P201 = ("P201", 6)
LIT201 = ("LIT201", 7)
P202 = ("P202", 8)
# SPHINX_SWAT_TUTORIAL TAGS)


class SwatProcess(Process):
    def pre_loop(self):
        print('[MiniNet Script] DEBUG: swat-s2 SwatProcess enters pre_loop at ' + str(datetime.datetime.now()))

        self.level_101 = self.set(LIT101, 0.500)
        self.level_201 = self.set(LIT201, 1)
        self.section = TANK_SECTION

    def main_loop(self):
        count = 0
        while count <= PP_SAMPLES:

            new_level_101 = self.level_101
            new_level_201 = self.level_201

            # compute water volume
            water_volume_101 = self.section * new_level_101
            water_volume_201 = self.section * new_level_201

            # inflows volumes
            mv101 = self.get(MV101)
            if float(mv101) == 1:
                self.set(FIT101, PUMP_FLOWRATE_IN)
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume_101 += inflow
            else:
                self.set(FIT101, 0.00)

            # outflows volumes
            p201 = self.get(P201)
            if float(p201) == 1:
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                print("[MiniNet Script] DEBUG RawWaterTank outlow lit101 inflow lit201: " + str(outflow))
                water_volume_101 -= outflow
                water_volume_201 += outflow

            p202 = self.get(P202)
            if float(p202) == 1:
                outflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                print("[MiniNet Script] DEBUG RawWaterTank outflow 201: " + str(outflow))
                water_volume_201 -= outflow

            # compute new water_level
            new_level_101 = water_volume_101 / self.section
            new_level_201 = water_volume_201 / self.section

            # level cannot be negative
            if new_level_101 <= 0.0:
                new_level_101 = 0.0
            if new_level_201 <= 0.0:
                new_level_201 = 0.0

            # update internal and state water level
            print("DEBUG new_level_101: " + str(new_level_101) + " \t delta: " + str(new_level_101 - self.level_101))
            print("DEBUG new_level_201: " + str(new_level_201) + " \t delta: " + str(new_level_201 - self.level_201))

            self.level_101 = self.set(LIT101, new_level_101)
            self.level_201 = self.set(LIT201, new_level_201)
            # 988 sec starting from 0.500 m
            # if new_level_101 >= LIT_101_M['HH']:
            #     # print 'DEBUG 101 above HH count: ', count
            #     break

            # # 367 sec starting from 0.500 m
            # elif new_level_101 <= LIT_101_M['LL']:
            #     # print 'DEBUG 101 below LL count: ', count
            #     break

            # if new_level_201 >= LIT_201_M['HH']:
            #     # print 'DEBUG 201 above HH count: ', count
            #     break

            # # 367 sec starting from 0.500 m
            # elif new_level_201 <= LIT_201_M['LL']:
            #     # print 'DEBUG 201 below LL count: ', count
            #     break


            time.sleep(PP_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ---------" + str(count) + "--------------\n\n\n")
        print('[MiniNet Script] DEBUG swat-s2 SwatProcess shutdown at ' + str(datetime.datetime.now()))


if __name__ == "__main__":

    rwt = SwatProcess(name="phy_pro", state=STATE)

import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV3_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN
from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES

import time

DEV3_ADDR = IP['dev3']

LIT101 = ('LIT101', 5)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev3(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev3 enters pre_loop at ' + str(datetime.datetime.now()))
        self.new_level = float(self.get(LIT101))
        self.send(LIT101, self.new_level, DEV3_ADDR)
        time.sleep(sleep)


    def main_loop(self):
        """mv101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print('[MiniNet Script] DEBUG: swat-s2 dev2 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            self.new_level = float(self.get(LIT101))
            self.send(LIT101, self.new_level, DEV3_ADDR)

            print('[MiniNet Script] DEBUG: swat-s2 lit101 level.', self.new_level)

            time.sleep(PLC_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")

        print('[MiniNet Script] DEBUG swat-s2 dev3 shutdown at ' + str(datetime.datetime.now()))
        self._stop()


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev3 = SwatDev3(
        name='dev3',
        state=STATE,
        protocol=DEV3_PROTOCOL)

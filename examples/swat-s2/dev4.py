import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV4_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN

import time

DEV4_ADDR = IP['dev4']

P201 = ('P201', 6)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev4(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev4 enters pre_loop at ' + str(datetime.datetime.now()))
        time.sleep(sleep)

    def main_loop(self):
        """p201 main loop.

            - reads sensors value
            - updates its enip server
        """

        print('DEBUG: swat-s2 dev4 enters main_loop.')
        print
                
                
        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            p201_1 = float(self.receive(P201, DEV4_ADDR))
            print('[MiniNet Script] P301 value: ' + str(p201_1))
            self.set(P201, p201_1)

            count += 1
            time.sleep(PLC_PERIOD_SEC)
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")

        print('[MiniNet Script] DEBUG swat-s2 dev4 shutdown at ' + str(datetime.datetime.now()))
        self._stop()


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev4 = SwatDev4(
        name='dev4',
        state=STATE,
        protocol=DEV4_PROTOCOL)
import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV6_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP

import time

DEV6_ADDR = IP['dev6']

P202 = ('P202', 8)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev6(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev6 enters pre_loop at ' + str(datetime.datetime.now()))
        time.sleep(sleep)

    def main_loop(self):
        """p202 main loop.

            - reads sensors value
            - updates its enip server
        """

        print('[MiniNet Script] DEBUG: swat-s2 dev6 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            p202_1 = float(self.receive(P202, DEV6_ADDR))
            print('[MiniNet Script] P301 value: %u'%p202_1)
            self.set(P202, p202_1)

            time.sleep(PLC_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")


        print('[MiniNet Script] DEBUG swat-s2 dev6 shutdown at ' + str(datetime.datetime.now()))
        self._stop()


if __name__ == "__main__":
    # notice that memory init is different form disk init
    dev4 = SwatDev6(
        name='dev6',
        state=STATE,
        protocol=DEV6_PROTOCOL)
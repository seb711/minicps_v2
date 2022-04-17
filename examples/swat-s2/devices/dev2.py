import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV2_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP

import time

DEV2_ADDR = IP['dev2']

MV101 = ('MV101', 4)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev2(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev2 enters pre_loop at ' + str(datetime.datetime.now()))


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
            mv101_1 = float(self.receive(MV101, DEV2_ADDR))
            self.set(MV101, mv101_1)

            print('[MiniNet Script] MV101 value: %u'%mv101_1
)

            time.sleep(PLC_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")

        print('[MiniNet Script] DEBUG swat-s2 dev2 shutdown at ' + str(datetime.datetime.now()))
        self._stop()


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev2 = SwatDev2(
        name='dev2',
        state=STATE,
        protocol=DEV2_PROTOCOL)

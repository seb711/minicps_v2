import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV5_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import STATE

import time

DEV5_ADDR = IP['dev5']

LIT201 = ('LIT201', 7)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev5(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev5 enters pre_loop at ' + str(datetime.datetime.now()))

    def main_loop(self):
        """lit201 main loop.

            - reads sensors value
            - updates its enip server
        """

        print('[MiniNet Script] DEBUG: swat-s2 dev5 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            self.new_level = float(self.get(LIT201))
            self.send(LIT201, self.new_level, DEV5_ADDR)

            print('[MiniNet Script] DEBUG LIT201 level: ', self.new_level)
            time.sleep(PLC_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")

        print('[MiniNet Script] DEBUG swat-s2 dev5 shutdown at ' + str(datetime.datetime.now()))
        self._stop()


if __name__ == "__main__":
    # notice that memory init is different form disk init
    dev5 = SwatDev5(
        name='dev5',
        state=STATE,
        protocol=DEV5_PROTOCOL)

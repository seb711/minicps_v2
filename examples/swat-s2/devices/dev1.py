import datetime
from minicps.devices import FieldDevice
from utils import STATE, DEV1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP

import time

DEV1_ADDR = IP['dev1']

FIT101 = ('FIT101', 3)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev1(FieldDevice):

    def pre_loop(self, sleep=0.1):
        print('[MiniNet Script] DEBUG: swat-s2 dev1 enters pre_loop at ' + str(datetime.datetime.now()))
        start_value = 0
        self.send(FIT101, start_value, DEV1_ADDR)
        time.sleep(sleep)

    def main_loop(self):
        """fit101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print('[MiniNet Script] DEBUG: swat-s2 dev1 enters main_loop.')

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS VALUE SHOULD NOT DEPEND FROM MV101 but normal deviations
            fit101 = float(self.get(FIT101))

            print('[MiniNet Script] DEBUG dev1 fit101: %.5f' % fit101)
            self.send(FIT101, fit101, DEV1_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1
            print("[MiniNet Script] ----- count: " + str(count) + "------------------")


        print('[MiniNet Script] DEBUG swat-s2 dev1 shutdown at ' + str(datetime.datetime.now()))
        self._stop()



if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev1 = SwatDev1(
        name='dev1',
        state=STATE,
        protocol=DEV1_PROTOCOL)

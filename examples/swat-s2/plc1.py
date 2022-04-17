"""
swat-s1 plc1.py
"""

import datetime
from minicps.devices import Controller
from utils import STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M
import time

PLC1_ADDR = IP["plc1"]

FIT101_PLC = ("FIT101", 1)
MV101_PLC = ("MV101", 1)
LIT101_PLC = ("LIT101", 1)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC1(Controller):
    def pre_loop(self, sleep=0.1):
        print(
            "[MiniNet Script] DEBUG: swat-s2 plc1 enters pre_loop at "
            + str(datetime.datetime.now())
        )
        print
        self.send(MV101_PLC, 1, PLC1_ADDR)
        self.send_intercom(MV101_PLC, 1, PLC1_ADDR)
        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

        - reads sensors value
        - drives actuators according to the control strategy
        - updates its enip server
        """
        count = 0
        while count <= PLC_SAMPLES:

            # lit101 [meters]
            lit101 = float(self.receive(LIT101_PLC, PLC1_ADDR))
            fit101 = float(self.receive(FIT101_PLC, PLC1_ADDR))
            print("[MiniNet Script] DEBUG plc1 lit101:" + str(lit101) + "\n")
            print("[MiniNet Script] DEBUG plc1 fit101:" + str(fit101) + "\n")
            self.send_intercom(LIT101_PLC, lit101, PLC1_ADDR)
            self.send_intercom(FIT101_PLC, fit101, PLC1_ADDR)

            if lit101 >= LIT_101_M["HH"]:
                print(
                    "[MiniNet Script] WARNING PLC1 - lit101 over HH: %.2f >= %.2f."
                    % (lit101, LIT_101_M["HH"])
                )

            if lit101 >= LIT_101_M["H"]:
                # CLOSE mv101
                print("[MiniNet Script] INFO PLC1 - lit101 over H -> close mv101.\n")
                self.send(MV101_PLC, 0, PLC1_ADDR)
                self.send_intercom(MV101_PLC, 0, PLC1_ADDR)

            elif lit101 <= LIT_101_M["LL"]:
                print(
                    "[MiniNet Script] WARNING PLC1 - lit101 under LL: %.2f <= %.2f."
                    % (lit101, LIT_101_M["LL"])
                )
            elif lit101 <= LIT_101_M["L"]:
                # OPEN mv101
                print("[MiniNet Script] INFO PLC1 - lit101 under L -> open mv101.\n")
                self.send(MV101_PLC, 1, PLC1_ADDR)
                self.send_intercom(MV101_PLC, 1, PLC1_ADDR)

            count += 1
            print("[MiniNet Script] ---------" + str(count) + "--------------\n\n\n")
            time.sleep(PLC_PERIOD_SEC)

        print(
            "[MiniNet Script] DEBUG swat-s2 plc1 shutdown at "
            + str(datetime.datetime.now())
        )
        self._stop()


if __name__ == "__main__":
    # notice that memory init is different form disk init
    plc1 = SwatPLC1(name="plc1", protocol=PLC1_PROTOCOL)

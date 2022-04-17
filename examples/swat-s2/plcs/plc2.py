
"""
swat-s1 plc3
"""

import datetime
from minicps.devices import Controller
from utils import PLC2_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC,LIT_101_M, LIT_201_M
from utils import IP

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']

LIT101_PLC = ('LIT101', 1)

LIT201_PLC = ('LIT201', 2)
P201_PLC = ('P201', 2)
P202_PLC = ('P202', 2)

class SwatPLC2(Controller):

    def pre_loop(self, sleep=0.1):
        print(
            "[MiniNet Script] DEBUG: swat-s2 plc2 enters pre_loop at "
            + str(datetime.datetime.now())
        )
        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """
        count = 0
        while(count <= PLC_SAMPLES):
            lit101 = 0
            # lit101 [meters]
            try:
                t = float(self.receive_intercom(LIT101_PLC, PLC1_ADDR))
                lit101 = t
            except ValueError:
                print("[MiniNet Script] ValueError: Not a float \n")
            lit201 = float(self.receive(LIT201_PLC, PLC2_ADDR))
            print('[MiniNet Script] DEBUG plc2 lit201:' + str(lit201) + "\n")
            self.send_intercom(LIT201_PLC, lit201, PLC2_ADDR)

            if lit201 >= LIT_201_M['HH']:
                print("[MiniNet Script] WARNING PLC2 - lit101 over HH: %.2f >= %.2f." % (
                    lit201, LIT_201_M['HH']))

            if lit201 >= LIT_201_M['H'] or lit101 <= LIT_101_M['L']:
                # CLOSE mv101
                print("[MiniNet Script] INFO PLC2 - lit101 over H -> close mv101 and  open p101. \n")
                self.send(P201_PLC, 0, PLC2_ADDR)
                self.send_intercom(P201_PLC, 0,PLC2_ADDR)

            if ((count / PLC_PERIOD_SEC) // 30) % 2 == 1: 
                print("[MiniNet Script] INFO PLC2 - p202 open.\n")
                self.send(P202_PLC, 1, PLC2_ADDR)
                self.send_intercom(P202_PLC, 1,PLC2_ADDR)
            else:
                print("[MiniNet Script] INFO PLC2 - p202 close.\n")
                self.send(P202_PLC, 0, PLC2_ADDR)
                self.send_intercom(P202_PLC, 0,PLC2_ADDR)

            
            if lit201 <= LIT_201_M['LL']:
                print("[MiniNet Script] WARNING PLC2 - lit101 under LL: %.2f <= %.2f." % (
                    lit201, LIT_201_M['LL']))

            elif lit201 <= LIT_201_M['L']:
                # OPEN mv101
                print("[MiniNet Script] INFO PLC2 - lit101 under L -> open p201 and close p202.\n")
                self.send(P201_PLC, 1, PLC2_ADDR)
                self.send_intercom(P201_PLC, 1, PLC2_ADDR)
                self.send(P202_PLC, 0, PLC2_ADDR)
                self.send_intercom(P202_PLC, 0,PLC2_ADDR)

            # Fill tank to limit if possible
            if lit201 <= LIT_201_M['H'] and lit101 > LIT_101_M['L']: 
                self.send(P201_PLC, 1, PLC2_ADDR)
                self.send_intercom(P201_PLC, 1, PLC2_ADDR)

            count += 1
            time.sleep(PLC_PERIOD_SEC)
            print("[MiniNet Script] ---------" + str(count) + "--------------\n\n\n")

        print(
            "[MiniNet Script] DEBUG swat-s2 plc2 shutdown at "
            + str(datetime.datetime.now())
        )       
        self._stop()


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2(
        name='plc2',
        protocol=PLC2_PROTOCOL)

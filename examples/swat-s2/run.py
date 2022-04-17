"""
swat-s2 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from mininet.term import runX11

import time
import argparse

from topo import SwatTopo

import sys


class SwatS2CPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net, attack):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        (
            plc1,
            plc2,
            dev1,
            dev2,
            dev3,
            dev4,
            dev5,
            dev6,
            s1,
            scada,
            attacker,
        ) = self.net.get(
            "plc1",
            "plc2",
            "dev1",
            "dev2",
            "dev3",
            "dev4",
            "dev5",
            "dev6",
            "s1",
            "scada",
            "attacker",
        )

        attacks = {
            "dcp_tampering": "./attacks/data_tampering/dcp_tampering.py",
            # "pnio_tampering": "./attacks/data_tampering/pnio_tampering.py",
            "rpc_tampering": "./attacks/data_tampering/rpc_tampering.py",
            # "forging": "./attacks/alarm_injection.py",
            "dos": "./attacks/dos/dos.py",
            # "replay": "./attacks/replay/replay.py",
        }
        

        if attack != "standard": 
            attack_scenario = attacks[attack]
            attacker.popen(['mnexec', 'socat', 'TCP-LISTEN:6010,fork,reuseaddr', "EXEC:'mnexec -a 1 socat STDIO TCP\\:127.0.0.1\\:6010'"])
            attacker.popen(['mnexec', 'xterm', '-title', '"Node: attacker"', '-display', 'localhost:10.0', '-e', 'sudo python3 ' + attack_scenario])
            time.sleep(5)
            

        # SPHINX_SWAT_TUTORIAL RUN(
        dev1.popen("sudo python ./startup_scripts/dev1_starter.py &")
        dev2.popen("sudo python ./startup_scripts/dev2_starter.py &")
        dev3.popen("sudo python ./startup_scripts/dev3_starter.py &")
        dev4.popen("sudo python ./startup_scripts/dev4_starter.py &")
        dev5.popen("sudo python ./startup_scripts/dev5_starter.py &")
        dev6.popen("sudo python ./startup_scripts/dev6_starter.py &")

        # attacker.popen('sudo python3 attacks/data_tampering/port_stealing.py &')

        # time.sleep(15)
        time.sleep(2)

        # plc1.popen(['mnexec', 'socat', 'TCP-LISTEN:6010,fork,reuseaddr', "EXEC:'mnexec -a 1 socat STDIO TCP\\:127.0.0.1\\:6010'"])
        # plc1.popen(['mnexec', 'xterm', '-title', '"Node: plc1"', '-display', 'localhost:10.0', '-e', 'sudo python plc1.py'])
        plc1.popen("sudo python ./startup_scripts/plc1_starter.py &")

        time.sleep(2)

        # plc2.popen(['mnexec', 'socat', 'TCP-LISTEN:6010,fork,reuseaddr', "EXEC:'mnexec -a 1 socat STDIO TCP\\:127.0.0.1\\:6010'"])
        # plc2.popen(['mnexec', 'xterm', '-title', '"Node: plc2"', '-display', 'localhost:10.0', '-e', 'sudo python plc2.py'])
        plc2.popen("sudo python ./startup_scripts/plc2_starter.py &")

        time.sleep(2)

        # attacker.popen(['mnexec', 'socat', 'TCP-LISTEN:6010,fork,reuseaddr', "EXEC:'mnexec -a 1 socat STDIO TCP\\:127.0.0.1\\:6010'"])
        # attacker.popen(['mnexec', 'xterm', '-title', '"Node: attacker"', '-e', 'sudo python physical_process.py'])
        s1.popen("sudo python ./startup_scripts/physical_process_starter.py &")

        time.sleep(4)
        runX11(scada, "sudo python ./devices/scada.py")

        # SPHINX_SWAT_TUTORIAL RUN)

        CLI(self.net)

        net.stop()


if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    parser = argparse.ArgumentParser()
    parser.add_argument("attack", type=str, choices=["dcp_tampering", "rpc_tampering", "dos", "standard"], default="")
    args = parser.parse_args()

    swat_s2_cps = SwatS2CPS(name="swat_s2", net=net, attack=args.attack)

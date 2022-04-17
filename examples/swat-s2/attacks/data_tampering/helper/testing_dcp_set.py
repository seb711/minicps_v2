from scapy.all import *
import time

# from profinet_controller.protocol_machines.cpm.messages.pnio_ps import *
import scapy.all as scapy
from scapy.contrib.pnio import *
from scapy.contrib.pnio_dcp import *

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

def get_set_ip_msg(src, dst, ip, netmask="255.255.255.0", gateway="0.0.0.0"):
    ether = scapy.Ether(dst=dst, src=src, type=0x8892)

    pnio_msg = ProfinetIO(frameID=0xFEFD)

    pnio_dcp_set_ip = ProfinetDCP(
        service_id=0x04,
        service_type=DCP_REQUEST,
        xid=0x04,
        reserved=0,
        dcp_data_length=18,
        option=0x01,
        sub_option=0x02,
        dcp_block_length=14,
        block_qualifier=0x0000,
        ip=ip,
        netmask=netmask,
        gateway=gateway,
    )

    return ether / pnio_msg / pnio_dcp_set_ip

pkt = get_set_ip_msg("00:1D:9C:C7:B0:70", "00:1D:9C:C7:B0:11", ip="192.168.1.40")
scapy.sendp(pkt, iface="plc1-eth0")
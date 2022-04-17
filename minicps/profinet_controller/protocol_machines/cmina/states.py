from __future__ import annotations
from abc import ABC, abstractmethod
from protocol_machines.cmina.messages.sim_pnio_dcp import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

# the context class contains a _state that references the concrete state and setState method to change between states.
class Device:

    _state = None

    def __init__(self, state: CMINAState, iface: str, mac_address: str = ""):
        self.setState(state)
        self.iface = iface
        self.mac_address = mac_address
        self.name = ""
        self.ip = ""

    def setState(self, state: CMINAState):

        print(f"CMINA: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def abort(self):
        self._state.abort()

    def identify(self, name):
        return self._state.identify(name)

    def setName(self, name):
        return self._state.setName(name)

    def setIp(self, ip):
        return self._state.setIp(ip)

    def reset(self):
        return self._state.reset()

    # Service Methods
    def resetDevice(self):
        print("RESET DEVICE")
        self.mac_address = ""
        self.name = ""
        self.ip = ""

    def initDevice(self, name, mac):
        print("INIT DEVICE", name, mac)
        self.name = name
        self.mac_address = mac

    def setDeviceName(self, name):
        self.name = name

    def setDeviceIp(self, ip):
        self.ip = ip

    def getDeviceName(self):
        return self.name

    def getDeviceIp(self):
        return self.ip

    def getDeviceMac(self):
        return self.mac_address


class CMINAState(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context: Device):
        self._context = context

    @abstractmethod
    def abort(self):
        pass

    @abstractmethod
    def identify(self, name):
        pass

    @abstractmethod
    def setName(self, name):
        pass
    @abstractmethod
    def setIp(self, ip):
        pass

    @abstractmethod
    def reset(self):
        pass


class CMINAIdentifyState(CMINAState):
    def abort(self):
        return

    def identify(self, name):
        # Send identify message, and wait for response:
        mac_address_src = get_mac_address()
        ident_msg = get_ident_msg(src=mac_address_src, name_of_station=name)
        ans, _ = scapy.srp(
            ident_msg,
            iface=self.context.iface,
            timeout=5,
            multi=True,
            verbose=False,
            filter=f"ether src {self.context.mac_address}",
        )
        # PROBLEM: EVERY DEVICE RESPONDS, MULTIPLE DEVICES WILL RESPOND TO THIS MESSAGE
        dst_mac_address = ans[-1].answer["Ethernet"].src

        if dst_mac_address == mac_address_src or len(ans) < 2:
            # error:
            # set state to set_name with name
            print("NO DEVICE IDENTIFIED WITH MAC: ", self.context.mac_address)
            self.context.resetDevice()
            return ""
        else:
            # success:
            # set state to identified
            self.context.setState(CMINAIdentifiedState())
            # self.context.initDevice(name, dst_mac_address)
            return dst_mac_address

    def setName(self, name):
        return False

    def setIp(self, ip):
        return False

    def reset(self):
        mac_address_src = get_mac_address()
        ident_msg = get_reset_factory_msg(
            src=mac_address_src, dst=self.context.getDeviceMac()
        )
        ans, _ = scapy.srp(
            ident_msg,
            iface=self.context.iface,
            timeout=5,
            multi=True,
            verbose=False,
            filter=f"ether src {self.context.mac_address}",
        )
        self.context.resetDevice()
        ans[-1].answer.show()


class CMINAIdentifiedState(CMINAState):
    def abort(self):
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self):
        return self.context.getDeviceMac()

    def setName(self, name):
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip):
        self.context.setState(CMINAArpState())
        return self.context.setIp(ip)

    def reset(self):
        self.context.setStateCMINA(CMINAIdentifyState())
        return self.context.reset()


class CMINASetNameState(CMINAState):
    def abort(self):
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self, name):
        return self.context.getDeviceMac()

    def setName(self, name):
        mac_address_src = get_mac_address()

        ident_msg = get_set_name_msg(
            src=get_mac_address(), name_of_station=name, dst=self.context.mac_address
        )
        ans, _ = scapy.srp(
            ident_msg,
            iface=self.context.iface,
            timeout=5,
            multi=True,
            verbose=False,
            filter=f"ether src {self.context.mac_address}",
        )
        set_name_rsp = ans[-1].answer

        if not set_name_rsp.haslayer("Profinet DCP"):
            print("NAME COULD NOT BE SET WITH DEVICE: ", self.context.mac_address)
            self.abort()
            return False

        dcp_pkt = set_name_rsp["Profinet DCP"]

        # DCP_SERVICE_TYPE = 0x01: "Response Success"
        # DCP_SERVICE_ID = 0x04: "Set"
        if dcp_pkt.service_type != 0x01 or dcp_pkt.service_id != 0x04:
            self.abort()
            return False

        self.context.setDeviceName(name)
        self.context.setState(CMINAIdentifiedState())
        return True

    def setIp(self, ip):
        self.context.setState(CMINAArpState())
        return self.context.setIp(ip)

    def reset(self):
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()


class SetIpState(CMINAState):
    def abort(self):
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self, name):
        return self.context.getDeviceMac()

    def setName(self, name):
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip):
        set_ip_msg = get_set_ip_msg(
            src=get_mac_address(), dst=self.context.getDeviceMac(), ip=ip
        )
        ans, _ = scapy.srp(
            set_ip_msg,
            iface=self.context.iface,
            timeout=5,
            multi=True,
            verbose=False,
            filter=f"ether src {self.context.mac_address}",
        )

        ip_rsp = ans[-1].answer

        ip_rsp.show2()

        if not ip_rsp.haslayer("Profinet DCP"):
            print("IP COULD NOT BE SET WITH DEVICE: ", self.context.mac_address)
            self.abort()
            return False
        dcp_pkt = ip_rsp["Profinet DCP"]

        # DCP_SERVICE_TYPE = 0x01: "Response Success"
        # DCP_SERVICE_ID = 0x04: "Set"
        if dcp_pkt.service_type != 0x01 or dcp_pkt.service_id != 0x04:
            self.abort()
            return False

        self.context.setDeviceIp(ip)
        self.context.setState(CMINAIdentifiedState())
        return True

    def reset(self):
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()


class CMINAArpState(CMINAState):
    def abort(self):
        self.context.setState(CMINAIdentifyState())

    def identify(self):
        return self.context.getDeviceMac()

    def setName(self, name):
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip):
        # arp request
        arp_request_broadcast = get_check_arp_ip(ip)
        ans, _ = scapy.srp(
            arp_request_broadcast, timeout=2, verbose=False, iface=self.context.iface
        )

        if len(ans) == 0:
            self.context.setState(SetIpState())
            return self.context.setIp(ip)
        else:
            ipShowed = False
            for i in ans:
                if i.answer["Ethernet"].src == self.context.mac_address:
                    self.context.setState(CMINAIdentifiedState())
                    return True
                print(i.answer["ARP"].psrc, i.answer["ARP"].pdst, ip)
                ipShowed |= i.answer["ARP"].psrc == ip
                i.answer.show()
            self.context.setState(CMINAIdentifiedState())
            return ipShowed

    def reset(self):
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()

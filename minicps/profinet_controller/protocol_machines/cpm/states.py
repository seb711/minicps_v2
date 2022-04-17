from __future__ import annotations
from abc import ABC, abstractmethod

from numpy import float64
from protocol_machines.cpm.helper.watchdog_timer import Watchdog
from protocol_machines.cpm.helper.gsdml_parser import XMLDevice
from protocol_machines.cpm.messages.pnio_ps import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio import *

from state.SqliteState import SQLiteState

scapy.load_contrib("pnio")


class Consumer:

    _state = None

    def __init__(
        self,
        state: CPMState,
        iface: str,
        device: object,
        dst_adr: str,
        dbState: SQLiteState,
    ):
        self.setState(state)
        self.iface = iface
        self.device = device
        self.dst_adr = dst_adr
        self.dbState = dbState
        self.id = 1

    def setState(self, state: CPMState):

        print(f"CPM: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def receiveMsgs(self):
        return self._state.receiveMsgs()

    def stopReceiveMsgs(self):
        return self._state.stopReceiveMsgs()


class CPMState(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context: Consumer):
        self._context = context

    @abstractmethod
    def receiveMsgs(self):
        pass

    @abstractmethod
    def stopReceiveMsgs(self):
        pass

    @abstractmethod
    def abort(self):
        pass


class CPMReceiveState(CPMState):
    def __init__(self):
        super().__init__()

    def sniffMessages(self):
        t = threading.currentThread()

        def update_load(pkt):
            if pkt.haslayer("PROFINET IO Real Time Cyclic Default Raw Data"):
                message_data = parse_data_message(pkt, self.context.device)
                self.context.dbState._set(
                    ("DO8", self.context.id), int(message_data.input_data["data"][0][0])
                )
                self.context.dbState._set(
                    ("DO32", self.context.id),
                    struct.unpack("f", bytearray(message_data.input_data["data"][1]))[
                        0
                    ],
                )
                self.context.dbState._set(
                    ("DO64", self.context.id),
                    struct.unpack("d", bytearray(message_data.input_data["data"][2]))[
                        0
                    ],
                )
                self.watchdogTimer.reset()

            elif pkt.haslayer("ProfinetIO"):
                # TODO: In Case of Alarm Message change state to IDLE and fire event
                # TODO: Maybe make network event queue, which transfers messages to right
                # State Machine, dependent on in which states the machines are
                data = pkt.getlayer("ProfinetIO")
                if data.frameID == 0xFE01:
                    print("ALARM LOW")
                    self.context.setState(CPMIdleState())
                    t.do_run = False
                elif data.frameID == 0xFC01:
                    print("ALARM HIGH")
                    self.context.setState(CPMIdleState())
                    t.do_run = False
        
        def stopFilter(x): 
            return not getattr(t, "do_run", True)

        sniff(
            filter=f"ether src {self.context.dst_adr}",
            store=0,
            count=-1,
            prn=update_load,
            iface=self.context.iface,
            stop_filter=stopFilter
        )

    def abort(self):
        self.context.setState(CPMIdleState())
        return

    def handleTimeout(self): 
            print("[CPM] Watchdog Timer exceeded! No messages from IO-Device. Consumer stops...")
            self.context.dbState._set(
                    ("ACTIVE", self.context.id), 0.0,
            )
            self.sniffThread.do_run = False
            self.stopReceiveMsgs()

    def receiveMsgs(self):
        self.sniffThread = threading.Thread(target=self.sniffMessages, daemon = True)
        self.sniffThread.start()
        self.watchdogTimer = Watchdog(4, userHandler=self.handleTimeout, args=[])
            

    def stopReceiveMsgs(self):
        self.context.setState(CPMIdleState())
        self.watchdogTimer.stop()
        return True


class CPMIdleState(CPMState):
    def abort(self):
        return

    def receiveMsgs(self):
        self.context.setState(CPMReceiveState())
        return self.context.receiveMsgs()

    def stopReceiveMsgs(self):
        return True

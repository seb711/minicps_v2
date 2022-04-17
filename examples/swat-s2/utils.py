from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ldir="logs/",
    suffix="",
)

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81  # m.s^-2
TANK_DIAMETER = 1.38  # m
TANK_SECTION = 1.5  # m^2
PUMP_FLOWRATE_IN = 0.7  # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 0.8  # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100e-3
T_PLC_W = 100e-3

T_PP_R = 200e-3
T_PP_W = 200e-3
T_HMI_R = 100e-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    "LL": 250.0,
    "L": 500.0,
    "H": 800.0,
    "HH": 1200.0,
}
LIT_101_M = {  # raw water tank m
    "LL": 0.250,
    "L": 0.500,
    "H": 0.800,
    "HH": 1.600,
}

LIT_201_MM = {  # ultrafiltration tank mm
    "LL": 250.0,
    "L": 800.0,
    "H": 1000.0,
    "HH": 1200.0,
}
LIT_201_M = {  # ultrafiltration tank m
    "LL": 0.250,
    "L": 0.800,
    "H": 1.000,
    "HH": 1.600,
}

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 500

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
# SPHINX_SWAT_TUTORIAL PROCESS UTILS)

# topo {{{1
IP = {
    "plc1": "192.168.1.10",
    "plc2": "192.168.1.20",
    "dev1": "192.168.1.40",
    "dev2": "192.168.1.50",
    "dev3": "192.168.1.60",
    "dev4": "192.168.1.70",
    "dev5": "192.168.1.80",
    "dev6": "192.168.1.90",
    "attacker": "192.168.1.77",
    "scada": "192.168.1.66",
}

NETMASK = "/24"

MAC = {
    "plc1": "00:1D:9C:C7:B0:70",
    "plc2": "00:1D:9C:C8:BC:46",
    "dev1": "00:1D:9C:C7:B0:11",
    "dev2": "00:1D:9C:C8:BC:12",
    "dev3": "00:1D:9C:C8:BD:13",
    "dev4": "00:1D:9C:C7:B0:14",
    "dev5": "00:1D:9C:C8:BC:15",
    "dev6": "00:1D:9C:C8:BC:16",
    "attacker": "00:1D:9C:C8:BD:18",
    "scada": "00:1D:9C:C8:BD:20",
}

# IO-CONTROLER / PLCs
# SPHINX_SWAT_TUTORIAL PLC1 UTILS(
DEV1_TAGS = (("FIT101", 3, "REAL"),)
DEV1_SERVER = {
    "address": IP["dev1"],
    "mac": MAC["dev1"],
    "tags": DEV1_TAGS,
    "name": "dev1",
}
DEV1_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV1_SERVER}

DEV2_TAGS = (("MV101", 4, "INT"),)
DEV2_SERVER = {
    "address": IP["dev2"],
    "mac": MAC["dev2"],
    "tags": DEV2_TAGS,
    "name": "dev2",
}
DEV2_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV2_SERVER}

DEV3_TAGS = (("LIT101", 5, "REAL"),)
DEV3_SERVER = {
    "address": IP["dev3"],
    "mac": MAC["dev3"],
    "tags": DEV3_TAGS,
    "name": "dev3",
}
DEV3_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV3_SERVER}

DEV4_TAGS = (("P201", 6, "INT"),)
DEV4_SERVER = {
    "address": IP["dev4"],
    "mac": MAC["dev4"],
    "tags": DEV4_TAGS,
    "name": "dev4",
}
DEV4_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV4_SERVER}


DEV5_TAGS = (("LIT201", 7, "REAL"),)
DEV5_SERVER = {
    "address": IP["dev5"],
    "mac": MAC["dev5"],
    "tags": DEV5_TAGS,
    "name": "dev5",
}
DEV5_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV5_SERVER}

DEV6_TAGS = (("P202", 8, "INT"),)
DEV6_SERVER = {
    "address": IP["dev6"],
    "mac": MAC["dev6"],
    "tags": DEV6_TAGS,
    "name": "dev6",
}
DEV6_PROTOCOL = {"name": "pnio_d", "mode": 1, "server": DEV6_SERVER}


# IO-CONTROLER / PLCs
PLC1_TAGS = (
    ("FIT101", 1, "REAL"),
    ("MV101", 1, "INT"),
    ("LIT101", 1, "REAL"),
)
PLC1_SERVER = {
    "address": IP["plc1"],
    "tags": PLC1_TAGS,
    "devices": {"FIT101": DEV1_SERVER, "MV101": DEV2_SERVER, "LIT101": DEV3_SERVER},
    "name": "plc1",
}
PLC1_PROTOCOL = {"name": "pnio_c", "mode": 1, "server": PLC1_SERVER}

PLC2_TAGS = (
    ("LIT201", 2, "REAL"),
    ("P201", 2, "INT"),
    ("P202", 2, "INT"),
)
PLC2_SERVER = {
    "address": IP["plc2"],
    "tags": PLC2_TAGS,
    "devices": {"P201": DEV4_SERVER, "LIT201": DEV5_SERVER,"P202": DEV6_SERVER},
    "name": "plc2",
}
PLC2_PROTOCOL = {"name": "pnio_c", "mode": 1, "server": PLC2_SERVER}

# SCADA
# SCADA_TAGS are tags that the scada system displays the user
SCADA_TAGS = [
    {"value": ("FIT101", 1), "address": IP["plc1"]},
    {"value": ("MV101", 1), "address": IP["plc1"]},
    {"value": ("LIT101", 1), "address": IP["plc1"]},
    {"value": ("LIT201", 2), "address": IP["plc2"]},
    {"value": ("P201", 2), "address": IP["plc2"]},
    {"value": ("P202", 2), "address": IP["plc2"]},
]
SCADA_VALUES = {
    "FIT101": ("Flow Sensor Value of Sensor FIT101 (in l/s)", "l/s"),
    "MV101": ("Valve MV101 to open water flow (1: on, 0: off)", "1: on / 0: off"),
    "LIT101": ("Water Sensor LIT101 in Tank (in m)", "m"),
    "P201": ("Pump status of pump P201 (1: on, 0: off)", "1: on / 0: off"),
    "LIT201": ("Water Sensor LIT201 in Tank (in m)", "m"),
    "P202": ("Pump status of pump P202 (1: on, 0: off)", "1: on / 0: off"),
}

SCADA_SERVER = {
    "address": IP["scada"],
    "mac": MAC["scada"],
    "values": SCADA_TAGS,
    "tags": (),
    "name": "scada",
}
SCADA_PROTOCOL = {
    "name": "enip",
    "mode": 1,
    "server": SCADA_SERVER,
}  # mode 0 is no server

# state {{{1
# SPHINX_SWAT_TUTORIAL STATE(
PATH = "swat_s2_db.sqlite"
NAME = "swat_s2"
STATE = {"name": NAME, "path": PATH}
# SPHINX_SWAT_TUTORIAL STATE)

SCHEMA = """
CREATE TABLE swat_s2 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s2 VALUES ('FIT101',   3, '0');
    INSERT INTO swat_s2 VALUES ('MV101',    4, '0');
    INSERT INTO swat_s2 VALUES ('LIT101',   5, '0');
    INSERT INTO swat_s2 VALUES ('P201',   6, '0');
    INSERT INTO swat_s2 VALUES ('LIT201',   7, '0');
    INSERT INTO swat_s2 VALUES ('P202',   8, '0');
"""

PN_SCHEMA = """
CREATE TABLE profinet_device (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             REAL,
    PRIMARY KEY (name, pid)
);
"""

PN_SCHEMA_INIT = """
    INSERT INTO profinet_device VALUES ('DO8',  1, 0.0);
    INSERT INTO profinet_device VALUES ('DO32', 1, 0.0);
    INSERT INTO profinet_device VALUES ('DO64', 1, 0.0);
    INSERT INTO profinet_device VALUES ('DI8',  1, 0.0);
    INSERT INTO profinet_device VALUES ('DI32', 1, 0.0);
    INSERT INTO profinet_device VALUES ('DI64', 1, 0.0);
    INSERT INTO profinet_device VALUES ('ACTIVE', 1, 1.0);
"""

PN_NAME = "profinet_device"
PN_PATH = "profinet_device.sqlite"
PN_STATE = {"name": PN_NAME, "path": PN_PATH}

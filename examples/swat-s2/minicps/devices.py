"""
``devices`` module contains:

    - ``get`` and ``set`` physical process's API methods
    - ``send`` and ``receive`` network layer's API methods
    - the user input validation code

Any device can be initialized with any couple of ``state`` and
``protocol`` dictionaries.

List of supported protocols and identifiers:
    - Devices with no networking capabilities have to set ``protocol`` equal
        to ``None``.
    - Ethernet/IP subset through ``cpppo``, use id ``enip``
        - Mode 0: client only.
        - Mode 1: tcp enip server.
    - Modbus through ``pymodbus``, use id ``modbus``
        - Mode 0: client only.
        - Mode 1: tcp modbus server.

List of supported backends:
    - Sqlite through ``sqlite3``

The consistency of the system should be guaranteed by the
client, e.g., do NOT init two different PLCs referencing to two different
states or speaking two different industrial protocols.

Device subclasses can be specialized overriding their public methods
e.g., PLC ``pre_loop`` and ``main_loop`` methods.
"""

import time

from os.path import splitext

from minicps.states import SQLiteState, RedisState
from minicps.protocols import EnipProtocol, ModbusProtocol, PnioProtocolController, PnioProtocolDevice


class Device(object):

    """Base class."""

    # TODO: state dict convention (eg: multiple table support?)
    def __init__(self, name, protocol, disk={}, memory={}):
        """Init a Device object.

        :param str name: device name
        :param dict protocol: used to set up the network layer API
        :param dict state: used to set up the physical layer API
        :param dict disk: persistent memory
        :param dict memory: main memory

        ``protocol`` (when is not ``None``) is a ``dict`` containing 3 keys:

            - ``name``: addresses a str identifying the protocol name (eg:
              ``enip``)
            - ``mode``: int identifying the server mode (eg: mode equals
              ``1``)
            - ``server``: if ``mode`` equals ``0`` is empty,
                otherwise it addresses a dict containing the server information
                such as its address, and a list of data to serve.

        ``state`` is a ``dict`` containing 2 keys:

            - ``path``: full (LInux) path to the database (eg: /tmp/test.sqlite)
            - ``name``: table name

        Device construction example:

        >>> device = Device(
        >>>     name='dev',
        >>>     protocol={
        >>>         'name': 'enip',
        >>>         'mode': 1,
        >>>         'server': {
        >>>             'address': '10.0.0.1',
        >>>             'tags': (('SENSOR1', 1), ('SENSOR2', 1)),
        >>>             }
        >>>     state={
        >>>         'path': '/path/to/db.sqlite',
        >>>         'name': 'table_name',
        >>>     }
        >>> )

        """

        self._validate_inputs(name, protocol, disk, memory)

        self.name = name
        self.protocol = protocol

        self._init_protocol()
        self._start()
        self._stop()

    def _validate_inputs(self, name, protocol, disk, memory):

        # name string
        if type(name) is not str:
            raise TypeError('Name must be a string.')
        elif not name:
            raise ValueError('Name string cannot be empty.')

        # protocol dict
        if type(protocol) is not dict:
            if protocol is not None:
                raise TypeError('Protocol must be either None or a dict.')
        else:
            protocol_keys = protocol.keys()
            if (not protocol_keys) or (len(protocol_keys) != 3):
                raise KeyError('Protocol must contain 3 keys.')
            else:
                for key in protocol_keys:
                    if ((key != 'name') and
                            (key != 'mode') and
                            (key != 'server')):
                        raise KeyError('%s is an invalid key.' % key)

            # protocol['name']
            if type(protocol['name']) is not str:
                raise TypeError('Protocol name must be a string.')
            else:
                name = protocol['name']
                if (name != 'enip' and name != 'modbus' and name != 'pnio_d' and name != 'pnio_c'):
                    raise ValueError('%s protocol not supported.' % protocol)
            # protocol['mode']
            if type(protocol['mode']) is not int:
                raise TypeError('Protocol mode must be a int.')
            else:
                mode = protocol['mode']
                if (mode < 0):
                    raise ValueError('Protocol mode must be positive.')
            # protocol['server'] TODO

            # protocol['client'] TODO after adding it to the API

    # TODO: add optional process name for the server and log location
    def _init_protocol(self):
        """Bind device to network API."""

        if self.protocol is None:
            print 'DEBUG: %s has no networking capabilities.' % self.name
            pass
        else:
            name = self.protocol['name']
            if name == 'enip':
                self._protocol = EnipProtocol(self.protocol)
            elif name == 'modbus':
                self._protocol = ModbusProtocol(self.protocol)
            elif name == 'pnio_c':
                self._protocol = PnioProtocolController(self.protocol)
                self._intercom_protocol = EnipProtocol(self.protocol)
            elif name == 'pnio_d':
                self._protocol = PnioProtocolDevice(self.protocol)
            else:
                print 'ERROR: %s protocol not supported.' % self.protocol

    def _start(self):
        """Start a device."""

        print "TODO _start: please override me"

    def _stop(self):
        """Stop a device."""

        print "TODO _stop: please override me"

    def send(self, what, value, address, **kwargs):
        """Send (write) a value to another network host.

        ``kwargs`` dict is used to pass extra key-value pair according to the
        used protocol.

        :param tuple what: field[s] identifier[s]
        :param value: value to be setted
        :param str address: ``ip[:port]``

        :returns: ``None`` or ``TypeError`` if ``what`` is not a ``tuple``
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            self._protocol._send(what, value, address, **kwargs)


    def receive(self, what, address, **kwargs):
        """Receive (read) a value from another network host.

        ``kwargs`` dict is used to pass extra key-value pair according to the
        used protocol.

        :param tuple what: field[s] identifier[s]
        :param str address: ``ip[:port]``

        :returns: received value or ``TypeError`` if ``what`` is not a ``tuple``
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._protocol._receive(what, address, **kwargs)

    def receive_intercom(self, what, address, **kwargs):
        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            if self._intercom_protocol: 
                return self._intercom_protocol._receive(what, address, **kwargs)
            else: 
                return self._protocol._receive(what, address, **kwargs)

    def send_intercom(self, what, value, address, **kwargs):
        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            if self._intercom_protocol: 
                self._intercom_protocol._send(what, value, address, **kwargs)
            return


# TODO: rename pre_loop and main_loop?
class Controller(Device):

    """Programmable Logic Controller class.

    PLC provides:
        - network APIs: e.g., communicate with an IO Device
    """

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def _stop(self):
        self._protocol._stop()
        if self._intercom_protocol: 
            self._intercom_protocol._stop()

    def pre_loop(self, sleep=0.5):
        """PLC boot process.

        :param float sleep: second[s] to sleep before returning
        """

        print "TODO PLC pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """PLC main loop.

        :param float sleep: second[s] to sleep after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO PLC main_loop: please override me"
            time.sleep(sleep)

            sec += 1

# TODO: rename pre_loop and main_loop?
class Scada(Device):

    """Scada class.

    Scada provides:
        - nothing
    Scada receices: 
        - values of PLCs
    """

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def _stop(self):
        pass

    def pre_loop(self, sleep=0.5):
        """SCADA boot process.

        """

        print "TODO PLC pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """SCADA main loop.

        """

        sec = 0
        while(sec < 1):

            print "TODO PLC main_loop: please override me"
            time.sleep(sleep)

            sec += 1

# TODO: rename pre_loop and main_loop?
class FieldDevice(Device):

    """Programmable Logic Controller class.

    IO Device provides:
        - state APIs: e.g., drive an actuator
        - network APIs: e.g., communicate with an IO Controller
    """
    # TODO: state dict convention (eg: multiple table support?)
    def __init__(self, name, protocol, state, disk={}, memory={}):
        # Added State to FieldDevice
        self._validate_state(state)
        self.state = state
        self._init_state()
        super(FieldDevice, self).__init__(name, protocol, disk, memory)


    def _validate_state(self, state): 
        # state dict
        if type(state) is not dict:
            raise TypeError('State must be a dict.')
        else:
            state_keys = state.keys()
            if (not state_keys) or (len(state_keys) != 2):
                raise KeyError('State must contain 2 keys.')
            else:
                for key in state_keys:
                    if (key != 'path') and (key != 'name'):
                        raise KeyError('%s is an invalid key.' % key)
            state_values = state.values()
            for val in state_values:
                if type(val) is not str:
                    raise TypeError('state values must be strings.')
            # state['path']
            subpath, extension = splitext(state['path'])
            # print 'DEBUG subpath: ', subpath
            # print 'DEBUG extension: ', extension
            if (extension != '.redis') and (extension != '.sqlite'):
                raise ValueError('%s extension not supported.' % extension)
            # state['name']
            if type(state['name']) is not str:
                raise TypeError('State name must be a string.')

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def _stop(self):
        self._protocol._stop()


    def set(self, what, value):
        """Set (write) a physical process state value.

        The ``value`` to be set (Eg: drive an actuator) is identified by the
        ``what`` tuple, and it is assumed to be already initialize. Indeed
        ``set`` is not able to create new physical process values.

        :param tuple what: field[s] identifier[s]
        :param value: value to be setted

        :returns: setted value or ``TypeError`` if ``what`` is not a ``tuple``
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._state._set(what, value)

    def get(self, what):
        """Get (read) a physical process state value.

        :param tuple what: field[s] identifier[s]

        :returns: gotten value or ``TypeError`` if ``what`` is not a ``tuple``
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._state._get(what)

    def _init_state(self):
        """Bind device to the physical layer API."""

        subpath, extension = splitext(self.state['path'])

        if extension == '.sqlite':
            # TODO: add parametric value filed
            print 'DEBUG state: ', self.state
            self._state = SQLiteState(self.state)
        elif extension == '.redis':
            # TODO: add parametric key serialization
            self._state = RedisState(self.state)
        else:
            print 'ERROR: %s backend not supported.' % self.state

    def pre_loop(self, sleep=0.5):
        """PLC boot process.

        :param float sleep: second[s] to sleep before returning
        """

        print "TODO PLC pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """PLC main loop.

        :param float sleep: second[s] to sleep after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO PLC main_loop: please override me"
            time.sleep(sleep)

            sec += 1

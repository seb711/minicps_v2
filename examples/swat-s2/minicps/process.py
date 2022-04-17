import time

from os.path import splitext

from minicps.states import SQLiteState, RedisState
from minicps.protocols import EnipProtocol, ModbusProtocol, PnioProtocolController, PnioProtocolDevice


class Process(object):

    """Base class."""

    # TODO: state dict convention (eg: multiple table support?)
    def __init__(self, name, state):
        """Init a Device object.

        :param str name: device name
        :param dict protocol: used to set up the network layer API
        :param dict state: used to set up the physical layer API
        :param dict disk: persistent memory
        :param dict memory: main memory

        ``protocol`` (when is not ``None``) is a ``dict`` containing 3 keys:

        """

        self._validate_inputs(name)

        self.name = name

        self._validate_state(state)
        self.state = state
        self._init_state()
        self._start()
        self._stop()

    def _validate_inputs(self, name):

        # name string
        if type(name) is not str:
            raise TypeError('Name must be a string.')
        elif not name:
            raise ValueError('Name string cannot be empty.')

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

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def _stop(self):
        pass

    def pre_loop(self, sleep=0.5):
        """Process boot process.

        :param float sleep: second[s] to sleep before returning
        """

        print "TODO Process pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """Process main loop.

        :param float sleep: second[s] to sleep after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO Process main_loop: please override me"
            time.sleep(sleep)

            sec += 1
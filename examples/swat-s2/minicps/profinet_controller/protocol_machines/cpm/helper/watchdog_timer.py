from threading import Timer

class Watchdog(Exception):
    def __init__(self, timeout, userHandler=None, args=[]):  # timeout in seconds
        self.timeout = timeout
        self.args = args
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler, self.args)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler, self.args)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self
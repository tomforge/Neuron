import abc

class BaseModule(abc.ABC):
    """
    Abstract base class for modules. All modules should inherit from this.
    Implements a simple interface for I/O.
    """
    def __init__(self, router):
        self.router = router
        self.startup()

    @abc.abstractmethod
    def startup(self):
        """ Modules must implement the startup() method, for any initialization
        when starting up """
        pass

    @abc.abstractmethod
    def shutdown(self):
        """ Modules must implement the shutdown() method, for any cleaning
        up when shutting down """
        pass

    @abc.abstractmethod
    def notify(self, eventType, data, sender):
        """ Modules must implement their own notify()
        method """
        pass

    def emit(self, eventType, data, addr=None):
        self.router.triggerEvent(eventType, data, addr)

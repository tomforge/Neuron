import abc

class BaseModule(abc.ABC):
    """
    Abstract base class for modules. All modules should inherit from this.
    Implements a simple interface for I/O.
    """
    def __init__(self, router):
        self.router = router

    def emit(self, eventType, data):
        self.router.triggerEvent(eventType, data)

    @abc.abstractmethod
    def receive(self, eventType, data):
        """ Modules must implement their own receive()
        method """
        pass

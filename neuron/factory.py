import logging

logger = logging.getLogger("server")
from autobahn.twisted.websocket import WebSocketServerFactory
from neuron import utils


class WSManagerFactory(WebSocketServerFactory):
    """
    Manages all websocket clients and connections. All
    interactions with clients should be made through this class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # A map of connected clients' addresses to their protocol instances
        self.clients = {}
        # A map of subscribers to their set of subscribed events
        self.subscribers = {}
        # A map of events to their set of subscribers
        self.eventSubscriptions = {}

    def registerClient(self, client):
        self.clients[client.peer] = client

    def unregisterClient(self, client):
        try:
            self.clients.pop(client.peer)
        except KeyError:
            logger.error(
                "Unregistering a client that was never registered: {}".format(client.peer))

    def addSubscription(self, subscriber, event):
        """
        Subscribe the given subscriber to the given event.
        Whenever the given event is received, the subscriber
        will be notified via the notify() function
        """
        if subscriber not in self.subscribers:
            self.subscribers[subscriber] = {event}
        else:
            self.subscribers[subscriber].add(event)

        if event not in self.eventSubscriptions:
            self.eventSubscriptions[event] = {subscriber}
        else:
            self.eventSubscriptions[event].add(subscriber)

    def removeSubscription(self, subscriber, event=None):
        """
        Stop notifying the given subscriber about the given event.
        If event is None, remove subscriber from all events.
        """
        try:
            if event is None:
                events = self.subscribers.pop(subscriber)
                for event in events:
                    self.eventSubscriptions[event].remove(subscriber)
                    if not self.eventSubscriptions[event]:
                        self.eventSubscriptions.pop(event)
            else:
                self.subscribers[subscriber].remove(event)
                if not self.subscribers[subscriber]:
                    self.subscribers.pop(subscriber)
                self.eventSubscriptions[event].remove(subscriber)
                if not self.eventSubscriptions[event]:
                    self.eventSubscriptions.pop(event)
        except KeyError:
            logger.error("Trying to remove non-existing subscription of "
                         + str(subscriber)
                         + ("" if event is None else " to " + str(event)))

    def dispatchToSubscribers(self, event, data, sender):
        """
        This is the main router function for client side events. All
        client events will be handled here and dispatched to
        backend subscribers.
        Raises:
            KeyError: If event is not in events list
        """
        try:
            for subscriber in self.eventSubscriptions[event]:
                try:
                    subscriber.notify(event, data, sender.peer)
                except (AttributeError, TypeError) as e:
                    logger.error(str(e))
        except KeyError:
            logger.warning("Received unsubscribed event " + str(event)
                           + " from " + sender.peer)

    def triggerEvent(self, event, data, addr=None):
        """
        Sends an event to the client of the given address. If
        not address is given, the event is broadcasted to all clients
        """
        payload = utils.construct_event_json(event, data)
        logger.debug(payload)
        if addr is None:
            for _, client in self.clients.items():
                client.sendMessage(payload, isBinary=False)
        elif addr in self.clients:
            self.clients[addr].sendMessage(payload, isBinary=False)
        else:
            logger.error("Client {} disconnected. Message not sent".format(addr))

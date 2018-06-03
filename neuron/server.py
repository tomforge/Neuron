import json
import logging
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

from neuron import settings

logger = logging.getLogger("server")

class WSProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.wasOpen = False
        return super().__init__()

    def onConnect(self, request):
        logger.info("{} connected".format(request.peer))
        # TODO: Authentication here?  Multiple WS protocol?
        return None

    def onOpen(self):
        """
        Websocket handshake complete and a connection is opened.
        Register the client to factory so that it can send and
        receive messages
        """
        logger.info("WebSocket opened with {}".format(self.peer))
        self.wasOpen = True
        self.factory.registerClient(self)

    def onMessage(self, payload, isBinary):
        try:
            event, data = json.loads(payload.decode('utf8'))
            self.factory.dispatch(event, data, self)
        except (json.JSONDecodeError, ValueError):
            logger.warning("Received invalid message " + str(payload)
                            + " from " + str(self.peer))

    def onClose(self, wasClean, code, reason):
        logger.info("{} disconnected with code {}.".format(self.peer, code)
                    + ("" if reason is None else " Reason: {}".format(reason)))
        # Ignore attempted but unopened connections
        if self.wasOpen:
            self.factory.unregisterClient(self)
        super().onClose(wasClean, code, reason)

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
                except (AttributeError, TypeError):
                    logger.error("Subscriber " + str(subscriber)
                                  + " does not implement the 'notify(event, data, addr)' endpoint")
        except KeyError:
            logger.warning("Received unsubscribed event " + str(event)
                            + " from " + sender.peer)

    def constructPayload(event, data):
        """
        Helper function to construct a payload for sending to clients
        """
        return json.dumps([event, data], ensure_ascii=False).encode('utf8')

    def triggerEvent(self, event, data, addr=None):
        """
        Sends an event to the client of the given address. If
        not address is given, the event is broadcasted to all clients
        """
        payload = constructPayload(event, data)
        if addr is None:
            for _, client in self.clients.items():
                client.sendMessage(payload, isBinary = False)
        elif addr in self.clients:
            self.clients[addr].sendMessage(payload, isBinary=False)
        else:
            logger.error("Client {} disconnected. Message not sent".format(addr))

def run_server(hostname="127.0.0.1", port=8080):
    # Make twisted report logs with python logging module
    twisted_log = log.PythonLoggingObserver(loggerName="server")
    twisted_log.start()

    factory = WSManagerFactory()
    factory.protocol = WSProtocol
    factory.setProtocolOptions(**settings.AUTOBAHN_PROTOCOL_OPTIONS)
    factory.startFactory()
    wsResource = WebSocketResource(factory)

    # Set static file location
    root = File(settings.FRONTEND_DIR)

    # Add a path for websocket connection
    root.putChild(settings.WS_ROUTE.encode(), wsResource)

    site = Site(root)
    reactor.listenTCP(port, site, interface=hostname)
    reactor.run()
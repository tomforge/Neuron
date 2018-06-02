import sys
import os
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

class WSProtocol(WebSocketServerProtocol):
    
    def onConnect(self, request):
        print("{} connected".format(request.peer))
        # TODO: Authentication here?  Multiple WS protocol?
        return None

    def onOpen(self):
        """
        Websocket handshake complete and a connection is opened.
        Register the client to factory so that it can send and
        receive messages
        """
        print("WebSocket opened with {}".format(self.peer))
        self.factory.registerClient(self)

    def onMessage(self, payload, isBinary):
        try:
            event, data = json.loads(payload.decode('utf8'))
            self.factory.dispatch(event, data, self)
        except (json.JSONDecodeError, ValueError):
            logging.WARNING("Received invalid message " + str(payload)
                            + " from " + self.peer)

    def onClose(self, wasClean, code, reason):
        print("{} disconnected".format(self.peer))
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
        self.clients.pop(client.peer)

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
            logging.ERROR("Trying to remove non-existing subscription of "
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
                    logging.ERROR("Subscriber " + str(subscriber)
                                  + " does not implement the 'notify(event, data, addr)' endpoint")
        except KeyError:
            logging.WARNING("Received unrecognized event " + str(event)
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
            logging.ERROR("Client {} disconnected. Message not sent".format(addr))

def run_server(port=8080):
    log.startLogging(sys.stdout)
    factory = WSManagerFactory("ws://127.0.0.1:" + str(port))
    factory.protocol = WSProtocol
    factory.setProtocolOptions(**settings.AUTOBAHN_WEBSOCKET_SETTINGS)
    wsResource = WebSocketResource(factory)

    # Static files should be in the 'components' folder in the same
    # directory as this file
    path, _ = os.path.split(os.path.realpath(__file__))
    root = File(path + "/components")

    # Add a path for websocket connection
    root.putChild(b"ws", wsResource)

    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()
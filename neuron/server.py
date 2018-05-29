import sys
import os
import json
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

class SimpleProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connected: {}".format(request.peer))
        # TODO: Authentication here? Multiple WS protocol?
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
        self.sendMessage(payload, isBinary) # Echo the received message, for testing only
        try:
            msg = json.loads(payload.decode('utf8'))
            # TODO: dispatch the message
            # eventDispatcher.notify(msg)
        except json.JSONDecodeError:
            # Send invalid message error
            self.sendMessage("Invalid message format".encode('utf8'))
            pass

    def onClose(self, wasClean, code, reason):
        self.factory.unregisterClient(self)
        super().onClose(wasClean, code, reason)


class ManagerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = {}
        self.subscribers = {}

    def registerClient(self, client):
        self.clients[client.peer] = client

    def unregisterClient(self, client):
        self.clients.pop(client.peer)

    def addSubscriber(self, subscriber, events):
        # TODO
        pass

    def removeSubscriber(self, subscriber, events):
        # TODO
        pass

    def dispatch(self, msg):
        """
        Dispatch received client message to backend subscribers
        """
        # TODO
        pass

    def broadcast(self, payload):
        """
        Broadcast backend message to all frontend clients
        """
        msg = json.dumps(payload, ensure_ascii = False).encode('utf8')
        for _, client in self.clients.items():
            client.sendMessage(msg, isBinary = False)

def run_server(port=8080):
    log.startLogging(sys.stdout)
    factory = ManagerFactory("ws://127.0.0.1:" + str(port))
    factory.protocol = SimpleProtocol
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
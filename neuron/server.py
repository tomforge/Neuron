import sys
import os

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource

from neuron.protocol import SimpleProtocol


def run_server(port=8080):
    log.startLogging(sys.stdout)
    wsFactory = WebSocketServerFactory("ws://127.0.0.1:" + str(port))
    wsFactory.protocol = SimpleProtocol
    wsResource = WebSocketResource(wsFactory)

    # Static files should be in the 'components' folder in the same
    # directory as this file
    path, _ = os.path.split(os.path.realpath(__file__))
    root = File(path + "/components")

    # Add a path for websocket connection
    root.putChild(b"ws", wsResource)

    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()

import sys
import os

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource

from neuron import protocol


def run_server(port=8080):
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory("ws://127.0.0.1:" + str(port))
    factory.protocol = protocol.SimpleProtocol
    resource = WebSocketResource(factory)

    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    root = File(path + "/plugins")
    root.putChild(b"ws", resource)

    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()

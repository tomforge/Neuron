import logging
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.resource import WebSocketResource

from neuron import settings

logger = logging.getLogger("server")

def run_server(router, hostname="127.0.0.1", port=8080):
    """
    Starts the event loop. All initialization should be done prior to
    calling this function. After this, the application will only respond
    to events.
    """
    # Make twisted report logs with python logging module
    twisted_log = log.PythonLoggingObserver(loggerName="server")
    twisted_log.start()

    # Wrap the router as a resource so we can expose it as an endpoint
    wsResource = WebSocketResource(router)

    # Set static file location
    root = File(settings.FRONTEND_DIR)

    # Attach the router to the File
    root.putChild(settings.WS_ROUTE.encode(), wsResource)

    site = Site(root)

    # Run forever
    reactor.listenTCP(port, site, interface=hostname)
    reactor.run()
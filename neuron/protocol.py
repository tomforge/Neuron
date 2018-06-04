import logging
logger = logging.getLogger("server")
import json
from autobahn.twisted.websocket import WebSocketServerProtocol


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
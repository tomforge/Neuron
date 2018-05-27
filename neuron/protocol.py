from autobahn.twisted.websocket import WebSocketServerProtocol
import json

class SimpleProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connected: {}".format(request.peer))
        # TODO: Authentication here? Multiple WS protocol?
        return None

    def onOpen(self):
        print("WebSocket opened")
        return super().onOpen()

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary) # Echo the received message, for testing only
        msg = json.loads(payload.decode('utf8'))
        # TODO: dispatch the message
        # eventDispatcher.notify(msg)

    def onClose(self, wasClean, code, reason):
        return super().onClose(wasClean, code, reason)


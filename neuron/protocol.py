from autobahn.twisted.websocket import WebSocketServerProtocol

class SimpleProtocol(WebSocketServerProtocol):
    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)
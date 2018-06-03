import logging
from neuron import server, settings, factory, protocol, utils

def main():
    """
    Entry point into the app.
    """
    # TODO: Handle user provided flags
    if(settings.DEBUG):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Set up the websocket factory. This is the central router
    # of the application, connecting the backend to the frontend clients
    router = factory.WSManagerFactory()
    router.protocol = protocol.WSProtocol
    router.setProtocolOptions(**settings.AUTOBAHN_PROTOCOL_OPTIONS)

    # TODO: Set up installed plugins
    plugins = map(utils.getClassInstanceFromPluginString, settings.INSTALLED_PLUGINS)


    server.run_server(router)

if __name__ == '__main__':
    main();
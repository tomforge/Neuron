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

    # Initialize modules
    modules = map(utils.get_class, settings.INSTALLED_MODULES)
    for module in modules:
        module(router)

    server.run_server(router)

if __name__ == '__main__':
    main();
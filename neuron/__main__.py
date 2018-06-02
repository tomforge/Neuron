import logging
from neuron import server, settings


def main():
    """
    Entry point into the app.
    """
    if(settings.DEBUG):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    # TODO: Set up installed plugins

    server.run_server()

if __name__ == '__main__':
    main();
import os

DEBUG = True

# Now we can construct paths with os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ERROR_LIST = {
    # TODO: figure out errors.. need to have a way to reserve events for core errors so no plugins can send them
    406 : "Not acceptable"
    }

INSTALLED_PLUGINS = [
    # TODO: Add plugins
    ]

AUTOBAHN_WEBSOCKET_SETTINGS = {
    "autoPingInterval" : 20,
    "autoPingTimeout" : 90
    }
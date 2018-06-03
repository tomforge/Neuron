import os

DEBUG = True

# Now we can construct paths with os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "components")

ERROR_LIST = {
    # TODO: figure out errors.. need to have a way to reserve events for core errors so no plugins can send them
    }

INSTALLED_PLUGINS = [
    # TODO: Add plugins
    ]

# 
# Websocket settings 
#

# The websocket endpoint, accessible at ws://<host>/<WS_ROUTE>
WS_ROUTE = "ws"

AUTOBAHN_PROTOCOL_OPTIONS = {
    "webStatus" : False, # Don't show webpage when users connect directly to ws endpoint without ws upgrade
    "autoPingInterval" : 20,
    "autoPingTimeout" : 90
    }
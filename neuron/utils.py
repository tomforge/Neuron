import importlib
def parsePluginString(plugin_string):
    """
    Parse plugin string (from neuron.settings)
    into module name and class name
    """
    moduleName, className = plugin_string.rsplit('.', 1)
    return ("plugins." + moduleName, className)

def getClassFromPluginString(plugin_string):
    moduleName, className = parsePluginString(plugin_string)
    mod = importlib.import_module(moduleName)
    return getattr(mod, className)
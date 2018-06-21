import importlib
import json
def parseModuleString(module_string):
    """
    Parse module string (from neuron.settings)
    into module name and class name
    """
    moduleName, className = module_string.rsplit('.', 1)
    return ("neuron.modules." + moduleName, className)

def getClassFromModuleString(module_string):
    moduleName, className = parseModuleString(module_string)
    mod = importlib.import_module(moduleName)
    return getattr(mod, className)

def constructEventJSON(event, data):
    """
    Helper function to construct a payload for sending to clients
    """
    return json.dumps([event, data], ensure_ascii=False).encode('utf8')

from collections import deque
from neuron.modules.baseModule import BaseModule
import keras
import logging
import inspect

logger = logging.getLogger("KerasClientModule")


# Operations are either Layers (Keras class APIs) or tf.Tensors (Keras function APIs)
class Operation:
    TYPES = {
        type_name: op
        for type_name, op
        in inspect.getmembers(keras.layers,
                              lambda x: (inspect.isclass(x) or inspect.isfunction(x)) and x.__name__[0].isupper())
    }

    def __init__(self, node):
        self.id = node["id"]
        self.name = node["name"]
        self.type = Operation.TYPES[node["type"]]
        self.op = self.build_op(node["params"])

    def __call__(self, *args, **kwargs):
        if self.istensor():
            # Tensor should not be called. This is a convenience function that simply returns the underlying tensor
            # to synchronize the tensor and layer API
            if args or kwargs:
                raise ValueError(
                    "Unsupported operation. Using {} as non-source node.".format(self.name))
            return self.op
        elif not args:
            raise ValueError("Unsupported operation. Using {} as source node (missing Input perhaps?).".format(self.name))

        return self.op(*args, **kwargs)

    def istensor(self):
        return inspect.isfunction(self.type)

    def islayer(self):
        return inspect.isclass(self.type)

    def build_op(self, params):
        # node params come in a list of the form [{"name": <param_name>, "value": <param_value>}, ... ]
        # Convert them to the form {<param_name>:<param_value> ... }
        parsed_params = {}
        for param in params:
            try:
                parsed_params[param["name"]] = None if (param["value"] is None or param["value"] == "") else eval(
                    param["value"], {}, {})
            except Exception as e:
                raise ValueError("Error parsing param {} of {}: {}".format(param["name"], self.name, str(e)))
        try:
            return self.type(**parsed_params)
        except Exception as e:
            raise ValueError("Error in node {}: {}".format(self.name, str(e)))


class KerasClientModule(BaseModule):
    # Data structure:
    # <Graph> := {"nodes": [<Node>], "edges": [<Edge>]}
    # <Node> := {"id": int, "name": string, "type": string, "params": {string: expr}}
    # <Edge> := [{"src": <Node.id>}, {"target": <Node.id>}]

    def startup(self):
        self.id_to_op = {}
        self.id_to_tensor = {}
        self.adj_list = {}
        self.reverse_adj_list = {}
        self.inputs = []
        self.outputs = []
        self.router.addSubscription(self, "API_get_node_meta")
        self.router.addSubscription(self, "API_build_graph")
        logger.debug("Started up")

    def shutdown(self):
        pass

    def notify(self, eventType, data, sender):
        logger.debug("Received event: " + eventType + " from " + sender)
        if eventType == "API_get_node_meta":
            self.API_get_node_meta(sender)
        elif eventType == "API_build_graph":
            self.API_build_graph(data, sender)

    def clear_graph(self):
        self.id_to_tensor = {}
        self.adj_list = {}
        self.reverse_adj_list = {}
        self.id_to_op = {}

    def build_graph_meta(self, graph):
        for node in graph["nodes"]:
            logger.debug(node.items())
            self.id_to_op[node["id"]] = Operation(node)
            self.adj_list[node["id"]] = []
            self.reverse_adj_list[node["id"]] = []
        for edge in graph["edges"]:
            logger.debug(edge.items())
            self.adj_list[edge["source"]].append(edge["target"])
            self.reverse_adj_list[edge["target"]].append(edge["source"])

    def get_topo_ord(self):
        in_degrees = {}
        queue = deque()
        topo_ord = []
        for src, parents in self.reverse_adj_list.items():
            if not parents:
                queue.append(src)
            else:
                in_degrees[src] = len(parents)

        while queue:
            curr = queue.popleft()
            topo_ord.append(curr)
            for child in self.adj_list[curr]:
                in_degrees[child] -= 1
                if in_degrees[child] == 0:
                    queue.append(child)
        return topo_ord

    def API_run_graph(self, output_node, sender):
        pass

    def API_build_graph(self, graph, sender):
        try:
            self.clear_graph()
            self.build_graph_meta(graph)
            self.inputs = []
            self.outputs = []
            for node_id in self.get_topo_ord():
                op = self.id_to_op[node_id]
                # Retrieve the actual nodes built earlier in this loop
                arg_list = [self.id_to_tensor[i] for i in self.reverse_adj_list[node_id]]
                logger.debug(str(arg_list))
                tensor = op(*arg_list)
                self.id_to_tensor[node_id] = tensor
                if not self.adj_list[node_id]:
                    self.outputs.append(tensor)
                if not self.reverse_adj_list[node_id]:
                    self.inputs.append(tensor)

            if len(self.inputs) == 1:
                self.inputs = self.inputs[0]
            if len(self.outputs) == 1:
                self.outputs = self.outputs[0]
        except Exception as e:
            logger.error(str(e))
            self.emit("RES_error", str(e), sender)

    def API_get_node_meta(self, sender):
        """ Prepare a representation of the internal nodeList array for
        sending to clients"""
        res = []
        logger.debug("Getting node meta")
        for name, op in Operation.TYPES.items():
            node_type = {
                "type": name,
                "doc": op.__doc__,
                "params": [
                    {
                        "name": param_name,
                        "value": repr(param.default) if param.default is not inspect.Parameter.empty else None
                    } for param_name, param in inspect.signature(op).parameters.items() if param_name != "kwargs"
                ]
            }
            res.append(node_type)
        self.emit("RES_get_node_meta", res, sender)

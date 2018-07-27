from collections import deque
from neuron.modules.baseModule import BaseModule
import keras
import logging
import inspect
logger = logging.getLogger("KerasClientModule")


class KerasClientModule(BaseModule):
    # Data structure:
    # <Graph> := {"nodes": [<Node>], "edges": [<Edge>]}
    # <Node> := {"id": int, "type": string, "params": {string: expr}}
    # <Edge> := [{"src": <Node>}, {"dest": <Node>}]

    def startup(self):
        self.node_types = {name: op for name, op in inspect.getmembers(keras.layers, inspect.isclass)}
        self.id_to_op = {}
        self.id_to_node = {}
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
            self.API_build_graph(data)

    def clear_graph(self):
        self.id_to_node = {}
        self.adj_list = {}
        self.reverse_adj_list = {}
        self.id_to_op = {}

    def build_graph_meta(self, graph):
        for node in graph["nodes"]:
            logger.debug(node.items())
            self.id_to_op[node["id"]] = self.build_op(node)
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

    def build_op(self, node):
        try:
            # logger.debug("NODE TYPE: " + node["type"])
            # logger.debug("OP: " + str(self.node_types[node["type"]]))
            params = {}
            for k,v in node["params"].items():
                params[k] = None if v is None else eval(v, {}, {})
                # logger.debug(str(k) + ": " + str(v) + "; " + str(type(v)) + " -> " + str(type(params[k])))
            return self.node_types[node["type"]](**params)
        except Exception as e:
            logger.error(str(e))
            raise

    def API_run_graph(self, output_node):
        pass

    def API_build_graph(self, graph):
        self.clear_graph()
        self.build_graph_meta(graph)
        self.inputs = []
        self.outputs = []
        for node_id in self.get_topo_ord():
            # Retrieve the actual nodes built earlier in this loop
            arg_list = [self.id_to_node[i] for i in self.reverse_adj_list[node_id]]
            node = self.id_to_op[node_id](*arg_list)
            self.id_to_node[node_id] = node

            if not self.adj_list[node_id]:
                self.outputs.append(node)
            if not self.reverse_adj_list[node_id]:
                self.inputs.append(node)
        if len(self.inputs) == 1:
            self.inputs = self.inputs[0]
        if len(self.outputs) == 1:
            self.outputs = self.outputs[0]

    def API_get_node_meta(self, sender):
        """ Prepare a representation of the internal nodeList array for
        sending to clients"""
        res = []
        logger.debug("Getting node meta")
        for name, op in self.node_types.items():
            params = {}
            for param_name, param in inspect.signature(op).parameters.items():
                if param_name == "kwargs":
                    continue
                if param.default == inspect.Parameter.empty:
                    params[param_name] = None
                else:
                    params[param_name] = repr(param.default)

            node_type = {
                "type": name,
                "doc": op.__doc__,
                "params": params
            }
            res.append(node_type)
        self.emit("RES_get_node_meta", res, sender)

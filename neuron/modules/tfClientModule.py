from collections import deque
from neuron.modules.baseModule import BaseModule
import tensorflow as tf
import logging
logger = logging.getLogger("TFClientModule")

class TFClientModule(BaseModule):
    # Data structure:
    #   - Edges
    #       - Tensor (don't need to store explicitly)
    #   - Nodes
    #       - Operation
    #       (Note: the following 3 are technically Operations that generate Tensors
    #       e.g. the Op `tf.constant(1)` creates a constant Tensor)
    #       - Constant
    #       - Variable
    #       - Placeholder (for data feed)
    #       - Compound nodes (essentially subgraphs, e.g. tf.layers)
    #
    # - Graph should stored as a dict of Nodes to a set of other Nodes
    # - Nodes should be stored with type, unique id, and any additional arguments
    #   required apart from input tensors)
    # Essentially, every node on UI should correspond to a TF (or self-defined) op
    #
    # Hence the final structure:
    # <Graph> = {<int> : <Node>} (mapping of Node id to Node object)
    # <Node>:
    #   Node.id = <int> (hashable unique identifier)
    #   Node.type = <string>
    #   Node.parents = [<int>] (parent node ids, stored in argument order - important for ops like '>=')
    #   Node.args = {<string> : <any>}

    def startup(self):
        self.nodeList = [tf.layers.conv2d, tf.layers.dense, tf.layers.max_pooling2d, tf.layers.dropout]
        self.router.addSubscription(self, "API_get_node_meta")
        logger.debug("Started up")

    def shutdown(self):
        pass

    def notify(self, eventType, data, sender):
        logger.debug("Received event: " + eventType + " from " + sender)
        if eventType == "API_get_node_meta":
            self.API_get_node_meta(sender)

    def constructInstSeq(self, graph):
        """
        Construct the sequence of instructions to be executed in order,
        to construct the actual graph in TF
        """
        edges = getEdges(graph)
        topoOrd = getTopoOrd(graph, edges)
        return [constructInstString(graph, node) for node in topoOrd]

    def getEdges(self, graph):
        edges = {}
        for id, node in graph.items():
            for nodeId in node.parents:
                if nodeId in forwardGraph:
                    edges[nodeId].add(id)
                else:
                    edges[nodeId] = {id}

        return edges

    def getTopoOrd(self, graph, edges):
        inDegrees = {}
        queue = deque()
        topoOrd = []
        for id, node in graph:
            if not node.parents:
                queue.append(node)
            else:
                inDegrees[id] = len(node.parents)
        while queue:
            curr = queue.popleft()
            topoOrd.append(curr)
            for childId in edges[curr.id]:
                inDegrees[childId] -= 1
                if inDegrees[childId] == 0:
                    queue.append(graph[childId])
        return topoOrd


    def constructInstString(self, graph, node):
        str = node.type + "("
        parentStr = ",".join([graph[id] for id in node.parents])
        argString = ",".join("{}:{}".format(param, args) for param,args in node.args)
        return ",".join([str, parentStr, argString])

    def API_get_node_meta(self, sender):
        """ Prepare a representation of the internal nodeList array for
        sending to clients"""
        res = []
        for idx, func in enumerate(self.nodeList):
            node = {
                "id": idx,
                "name": func.__name__,
                "doc": func.__doc__
            }
            res.append(node)
        logger.debug("OK")
        self.emit("RES_get_node_meta", res, sender)

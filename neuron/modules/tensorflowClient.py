from collections import deque
from neuron.modules import BaseModule

class tensorflowClient(BaseModule):
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
    apiList = [
      "ADAMS",
      "MAD",
      "ACES",
      "add",
      "subtract",
      "mult",
      "matmul",
      "dot",
      "conv"
    ]

    def constructInstSeq(graph):
        """
        Construct the sequence of instructions to be executed in order,
        to construct the actual graph in TF
        """
        edges = getEdges(graph)
        topoOrd = getTopoOrd(graph, edges)
        return [constructInstString(graph, node) for node in topoOrd]

    def getEdges(graph):
        edges = {}
        for id, node in graph.items():
            for nodeId in node.parents:
                if nodeId in forwardGraph:
                    edges[nodeId].add(id)
                else:
                    edges[nodeId] = {id}

        return edges

    def getTopoOrd(graph, edges):
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


    def constructInstString(graph, node):
        str = node.type + "("
        parentStr = ",".join([graph[id] for id in node.parents])
        argString = ",".join("{}:{}".format(param, args) for param,args in node.args)
        return ",".join([str, parentStr, argString])

    def API_get_node_meta():
        res = [{idx : val} for (idx, val) in enumerate(apiList)]
        self.emit("RES_get_node_meta", res)

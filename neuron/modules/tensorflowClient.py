class tensorflowClient:
    # Data structure:
    #   - Edges
    #       - Tensor (don't need to store explicitly)
    #   - Nodes
    #       - Operation
    #       (Note: the following 3 are technically Operations that generate Tensors
    #       e.g. the Op `tf.constant(1)` creates a constant Rensor)
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
    # <Graph> = {<Node> : {<Node>} }
    # <Node>:
    #   Node.id = <int>
    #   Node.type = <string>
    #   Node.args = {<string> : <any>}
    def constructInstSeq(graph):
        """
        Construct the sequence of instructions to be executed in order,
        to construct the actual graph in TF
        """
        # Do a topo sort on the Nodes in the graph
        # Construct the instruction string from the Nodes
        pass

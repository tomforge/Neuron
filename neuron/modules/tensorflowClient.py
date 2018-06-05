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
    #       - Graph (some graphs are also nodes if they accept a Tensor as input and
    #           outputs a tensor, especially grouping wrappers e.g. tf.layers)
    #               (Note: This is a representation of the dataflow graph, and is
    #               distinct from tf.Graph)
    # Graph should stored as a dict of Nodes to a set of other Nodes
    # Nodes should be stored with type, unique id, and any additional arguments 
    #   required apart from input tensors)
    # To compress a graph where there are potentially many identical groupings,
    #   sub-graphs should be defined first, then used as nodes in the final graph
    #
    # Hence the final structure:
    # Graph:
    #   Graph.id = int
    #   Graph.def = {set, Graph}
    #   Graph.full = {dict, Node : {set, Node} }
    # Node:
    #   Node.id = int
    #   Node.type = string
    #   Node.args = {dict, string : <any>}
    pass

import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

function NewWebSocketPlugin() {
  const wsuri = "ws://" + location.host + "/ws";
  const socket =
    "WebSocket" in window
      ? new WebSocket(wsuri)
      : "MozWebSocket" in window
        ? new MozWebSocket(wsuri)
        : null;

  return store => {
    //TODO: Throw alert when WebSocket is disconnected
    if (socket) {
      socket.onopen = () => store.commit("_SOCKET_CONNECT");
      socket.onclose = () => store.commit("_SOCKET_DISCONNECT");
      socket.onmessage = evt =>
        store.commit("_SOCKET_HANDLE_MESSAGE", JSON.parse(evt.data));
      // The plugin subscribes only to the "emit" mutation,
      // to send events to server
      store.subscribe(mutation => {
        if (mutation.type === "emit") {
          let jsonPayload = JSON.stringify(mutation.payload);
          // If not ready, wait 500ms before trying again. Only tries once more, if
          // connection is still not up, this message will be lost
          if (!socket.readyState) {
            setTimeout(() => socket.send(jsonPayload), 500);
          } else {
            socket.send(jsonPayload);
          }
        }
      });
    }
  };
}

function UndoRedoGraphPlugin(store) {
  let undoableMutations = [
    "addNode",
    "addEdge",
    "removeNodeGivenId",
    "removeEdge"
  ];
  let history = [];
  let present = {
    nodes: store.state.nodes.slice(),
    edges: store.state.edges.slice()
  };
  let future = [];
  function updateFlags() {
    // Update flags for API use
    store.commit("_SET_UNDOABLE", history.length > 0);
    store.commit("_SET_REDOABLE", future.length > 0);
  }
  store.subscribe((mutation, state) => {
    if (undoableMutations.includes(mutation.type)) {
      history.push(present);
      // Create new object with shallow copy of nodes + edges arrays
      present = {
        nodes: state.nodes.slice(),
        edges: state.edges.slice()
      };
      future = [];
      updateFlags();
    } else if (mutation.type === "undoGraph") {
      if (history.length > 0) {
        future.push(present);
        present = history.pop();
        store.commit("_SET_GRAPH", present);
        updateFlags();
      }
    } else if (mutation.type === "redoGraph") {
      if (future.length > 0) {
        history.push(present);
        present = future.pop();
        store.commit("_SET_GRAPH", present);
        updateFlags();
      }
    }
  });
}
export default new Vuex.Store({
  state: {
    wsConnected: false,
    wsPayload: "",
    nodeTypes: [
      {
        type: "test",
        params: {
          testParam1: 1,
          testParam2: "lorem"
        },
        doc: "test"
      }
    ],
    selectedNode: null,
    nodes: [],
    edges: [],
    undoable: false,
    redoable: false
  },
  mutations: {
    // SOCKET_ prefixed mutations should be called only
    // by the WebSocket plugin
    _SOCKET_CONNECT(state) {
      state.wsConnected = true;
    },
    _SOCKET_DISCONNECT(state) {
      state.wsConnected = false;
    },
    _SOCKET_HANDLE_MESSAGE(state, msg) {
      let [eventType, data] = msg;
      if (eventType === "RES_get_node_meta") {
        state.nodeTypes = data;
      }
    },
    _SET_GRAPH(state, graph) {
      state.nodes = graph.nodes.slice();
      state.edges = graph.edges.slice();
    },
    _SET_REDOABLE(state, redoable) {
      state.redoable = redoable;
    },
    _SET_UNDOABLE(state, undoable) {
      state.undoable = undoable;
    },
    emit() {},

    addNode(state, node) {
      state.nodes.push(node);
    },
    addEdge(state, edge) {
      state.edges.push(edge);
    },
    removeNodeGivenId(state, nodeId) {
      state.nodes = state.nodes.filter(n => n.name !== nodeId);
      // Remove associated edges
      state.edges = state.edges.filter(
        e => !(e.source === nodeId || e.target === nodeId)
      );
    },
    removeEdge(state, edge) {
      state.edges = state.edges.filter(
        e => !(e.source === edge.v && e.target === edge.w)
      );
    },
    selectNodeById(state, nodeId) {
      if (nodeId === null) {
        state.selectedNode = null;
      } else if (
        state.selectedNode === null ||
        state.selectedNode.name !== nodeId
      ) {
        state.selectedNode = state.nodes.find(n => n.name === nodeId);
      }
    },
    // Used for callbacks on UndoRedoGraphPlugin only
    undoGraph() {},
    redoGraph() {}
  },
  actions: {},
  plugins: [NewWebSocketPlugin(), UndoRedoGraphPlugin]
});

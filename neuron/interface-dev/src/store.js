import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

function createWebSocketPlugin() {
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
      socket.onopen = () => store.commit("SOCKET_CONNECT");
      socket.onclose = () => store.commit("SOCKET_DISCONNECT");
      socket.onmessage = msg => store.commit("SOCKET_HANDLE_MESSAGE", msg);
      // The plugin subscibes only to the "emit" mutation,
      // to send events to server
      store.subscribe(mutation => {
        if (mutation.type === "emit") {
          socket.send(mutation.wsPayload);
        }
      });
    }
  };
}

const wsPlugin = createWebSocketPlugin();

export default new Vuex.Store({
  state: {
    wsConnected: false,
    wsPayload: "",
    nodeTypes: [
      "adam's",
      "mad",
      "aces",
      "add",
      "subtract",
      "mult",
      "matmul",
      "dot"
    ]
  },
  mutations: {
    // SOCKET_ prefixed mutations should be called only
    // by the websocket plugin
    SOCKET_CONNECT(state) {
      state.wsConnected = true;
    },
    SOCKET_DISCONNECT(state) {
      state.wsConnected = false;
    },
    SOCKET_HANDLE_MESSAGE(state, msg) {
      // handle message here
    },
    emit(state, evt, data) {
      state.wsPayload = JSON.stringify([evt, data]);
    }
  },
  actions: {},
  plugins: [wsPlugin]
});

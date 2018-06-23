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
      socket.onmessage = evt =>
        store.commit("SOCKET_HANDLE_MESSAGE", JSON.parse(evt.data));
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

const wsPlugin = createWebSocketPlugin();

export default new Vuex.Store({
  state: {
    wsConnected: false,
    wsPayload: "",
    nodeTypes: [{"id":0, "name":"test1", "doc":"lorem ipsum dolor sit amet"}]
  },
  mutations: {
    // SOCKET_ prefixed mutations should be called only
    // by the WebsScket plugin
    SOCKET_CONNECT(state) {
      state.wsConnected = true;
    },
    SOCKET_DISCONNECT(state) {
      state.wsConnected = false;
    },
    SOCKET_HANDLE_MESSAGE(state, msg) {
      let [eventType, data] = msg;
      if (eventType === "RES_get_node_meta") {
        state.nodeTypes = data;
      }
    },
    emit(state, evt) {}
  },
  actions: {},
  plugins: [wsPlugin]
});

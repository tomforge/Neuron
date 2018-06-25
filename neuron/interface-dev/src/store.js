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
    nodeTypes: [{"id":0, "name":"test1", "doc":"lorem ipsum dolor sit amet"},
      {"id":1, "name":"test2", "doc":"lorem ipsum dolor sit amet"},
      {"id":2, "name":"test3", "doc":"lorem ipsum dolor sit amet"},
      {"id":3, "name":"test4", "doc":"lorem ipsum dolor sit amet"},
      {"id":4, "name":"test5", "doc":"lorem ipsum dolor sit amet"},
      {"id":5, "name":"test6", "doc":"lorem ipsum dolor sit amet"},
      {"id":6, "name":"test7", "doc":"lorem ipsum dolor sit amet"},
      {"id":7, "name":"test8", "doc":"lorem ipsum dolor sit amet"},
      {"id":8, "name":"test9", "doc":"lorem ipsum dolor sit amet"},
      {"id":9, "name":"test10", "doc":"lorem ipsum dolor sit amet"},
      {"id":10, "name":"test11", "doc":"lorem ipsum dolor sit amet"},
      {"id":11, "name":"test12", "doc":"lorem ipsum dolor sit amet"},
      {"id":12, "name":"test13", "doc":"lorem ipsum dolor sit amet"},
      {"id":13, "name":"test14", "doc":"lorem ipsum dolor sit amet"}]
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

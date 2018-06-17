import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
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
  mutations: {},
  actions: {}
});

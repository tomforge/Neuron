import Vue from "vue";
import Router from "vue-router";
import About from "./views/About.vue"
import Draw from "./views/Draw.vue";
import Run from "./views/Run.vue";
import Visualize from "./views/Visualize.vue";

Vue.use(Router);

export default new Router({
  routes: [
    // INITIAL ROUTE
    {
      path: "/",
      redirect: "/draw"
    },
    {
      path: "/about",
      name: "about",
      component: About
    },
    {
      path: "/draw",
      name: "draw",
      component: Draw
    },
    {
      path: "/run",
      name: "run",
      component: Run
    },
    {
      path: "/visualize",
      name: "visualize",
      component: Visualize
    },
    {
      path: "*",
      redirect: "/draw"
    }
  ]
});

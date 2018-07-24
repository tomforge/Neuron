<template>
<v-app id="inspire" dark>

  <v-system-bar status app lights-out>
    <v-spacer></v-spacer>
    <span class="headline text-xs-center">neuron</span>
    <v-spacer></v-spacer>
  </v-system-bar>
  <!--HEADER TOOLBAR-->
  <v-toolbar color="grey darken-3" dense fixed clipped-left app>
    <v-toolbar-title class="ml-3">
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-tabs fixed-tabs color="transparent">
        <v-tab v-for="view in mainViews" :to="view.link" :key="view.text">{{view.text}}</v-tab>
      </v-tabs>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-btn small color="primary" v-on:click.native="build_graph()">BUILD GRAPH</v-btn>
    <v-menu bottom left offset-y>
      <v-btn slot="activator" icon>
        <v-icon>settings</v-icon>
      </v-btn>
      <v-list>
        <router-link v-for="view in mainViews" :to="view.link" :key="view.text" tag="v-list-tile">
          <v-list-tile-content>
            <v-list-tile-title>{{view.text}}</v-list-tile-title>
          </v-list-tile-content>
        </router-link>
      </v-list>
    </v-menu>
    <v-menu bottom left offset-y>
      <v-btn slot="activator" icon>
        <v-icon>help_outline</v-icon>
      </v-btn>
      <v-list>
        <router-link to="/about" tag="v-list-tile">
          <v-list-tile-content>
            <v-list-tile-title>About</v-list-tile-title>
          </v-list-tile-content>
        </router-link>
        <router-link to="/faq" tag="v-list-tile">
          <v-list-tile-content>
            <v-list-tile-title>FAQ</v-list-tile-title>
          </v-list-tile-content>
        </router-link>
      </v-list>
    </v-menu>
  </v-toolbar>

  <!--MAIN VIEW WINDOW-->
  <v-content style="background-color: #212121;">
    <router-view></router-view>
  </v-content>
</v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      drawer: true,
      mainViews: [
        {
          link: "/draw",
          text: "DRAW"
        },
        {
          link: "/run",
          text: "RUN"
        },
        {
          link: "/visualize",
          text: "VISUALIZE"
        }
      ]
    };
  },
  methods: {
    build_graph() {
      this.$store.commit("emit", [
        "API_build_graph",
        {
          nodes: this.$store.state.nodes,
          edges: this.$store.state.edges
        }
      ]);
    }
  }
};
</script>

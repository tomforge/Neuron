<template>
<v-app id="inspire" dark>

  <!--HEADER TOOLBAR-->
  <v-toolbar color="amber darken-4" dense fixed clipped-left app>
    <v-toolbar-title class="mr-5 align-center">
      <span class="title">neuron</span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn v-for="view in mainViews" :to="view.link" :key="view.text" flat> {{view.text}}</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
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
  <v-content>
    <v-container fluid fill-height>
      <router-view></router-view>
    </v-container>
  </v-content>

</v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      drawer: true,
      items: [{
          icon: 'home',
          text: 'Adam\'s'
        },
        {
          icon: 'featured_play_list',
          text: 'Mad'
        },
        {
          icon: 'work',
          text: 'Aces'
        }
      ],
      mainViews: [{
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
        },
      ]
    }
  }
}
</script>

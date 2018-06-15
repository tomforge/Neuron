<template>
  <v-app
    id="inspire"
    dark
  >
    <v-navigation-drawer
      v-model="drawer"
      fixed
      clipped
      app
    >
      <v-list dense>
        <v-list-tile v-for="item in items" :key="item.text" @click="">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              {{ item.text }}
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-subheader class="mt-3 grey--text text--darken-1">HELLO WORLD</v-subheader>
		 <v-list-tile v-for="view in views" :key="view.text" @click="">
			<v-list-tile-content>
				<router-link :to="view.link" tag="v-list-tile-title" style="cursor:pointer">
					{{ view.text }}
				</router-link>
			</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="orange darken-1"
      dense
      fixed
      clipped-left
      app
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title class="mr-5 align-center">
        <span class="title">Neuron</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
	  
      <v-layout row align-center style="max-width: 650px">
        <v-text-field
          :append-icon-cb="() => {}"
          placeholder="Search..."
          single-line
          append-icon="search"
          color="white"
          hide-details
        ></v-text-field>
      </v-layout>
    </v-toolbar>
    <v-content>
      <v-container fill-height>
        <v-layout justify-center align-center>
          <v-flex shrink>
			<router-view></router-view>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      drawer: true,
      items: [
        { icon: 'trending_up', text: 'Adam\'s' },
        { icon: 'featured_play_list', text: 'Mad' },
        { icon: 'watch_later', text: 'Aces' }
      ],
	  views: [
		{ link: "/", text: "Home" },
		{ link: "/about", text: "About" }
	  ]
    }
  }
}
</script>

<template>
<div class="draw">
  <!-- LEFT DRAWER -->
  <v-navigation-drawer v-model="drawer" fixed clipped app :mini-variant.sync="mini">
    <v-btn icon @click.native.stop="mini = !mini">
      <v-icon>chevron_left</v-icon>
    </v-btn>
    <v-list dense>
      <v-subheader class="mt-3 grey--text text--darken-1">TENSORFLOW APIS</v-subheader>
      <v-list-tile>
        <v-text-field :append-icon-cb="() => {}" placeholder="Search..." single-line append-icon="search" color="white" hide-details></v-text-field>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
  <h1>draw page</h1>
</div>
</template>
<script>
export default {
  name: 'Draw',
  data() {
    return {
      drawer: true,
      mini: true
    }
  }
}
</script>

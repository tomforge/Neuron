<template>
<div class="draw">
  <!-- LEFT DRAWER -->
  <v-navigation-drawer v-model="drawer" fixed clipped app permanent stateless>
    <v-text-field class="pa-2" :append-icon-cb="() => {}" placeholder="Search"
       single-line append-icon="search" color="white" hide-details
       v-model="searchStr"></v-text-field>
    <v-list>
      <template v-for="item in filteredNodeTypes">
        <v-list-tile :key="item" @click="" color="grey lighten-1">
          <v-list-tile-content>
            <v-list-tile-title v-html="$options.filters.highlight(item, searchStr, 'white')">{{item}}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider></v-divider>
      </template>
    </v-list>
  </v-navigation-drawer>
  <svg id="board" width="1280px" height="960px"></svg>
</div>
</template>
<script>

import * as d3 from "d3";
import { mapState } from "vuex";

export default {
  name: 'Draw',
  data() {
    return {
      drawer: true,
      searchStr: "",
    }
  },
  computed: {
    // vuex states
    ...mapState({
      nodeTypes: "nodeTypes"
    }),

    filteredNodeTypes() {
      if(!this.searchStr) {
        return this.nodeTypes;
      } else {
        return this.nodeTypes.filter(
          // Return only word-boundary matches (e.g. don't return "add" if
          // searching for "d")
          nodeType => (nodeType.search("\\b" + this.searchStr) !== -1)
        );
      }
    }
  },

  mounted() {
    this.initBoard();
  },

  methods: {
    initBoard() {
      let svg = d3.select("svg").call(d3.zoom().on("zoom", function () {
        svg.attr("transform", d3.event.transform)
      })).append("g")

      svg.append("circle")
        .attr("cx", document.body.clientWidth / 2)
        .attr("cy", document.body.clientHeight / 2)
        .attr("r", 50)
        .style("fill", "#FFFFFF")
    }
  },

  filters: {
    highlight: function(str, toMatch, color) {
      var matcher = new RegExp(toMatch, "i");
      return str.replace(matcher,
        matched => ("<span style=\"color:" + color + "\">" + matched + "</span>"));
    }
  }
}
</script>

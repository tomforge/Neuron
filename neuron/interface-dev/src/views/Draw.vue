<template>
<div class="draw">
  <!-- LEFT DRAWER -->
  <v-navigation-drawer v-model="drawer" fixed clipped app permanent stateless>
    <v-text-field class="pa-2" :append-icon-cb="() => {}" placeholder="Search"
       single-line append-icon="search" color="white" hide-details
       v-model="searchStr" @input="filterSearchResults"></v-text-field>
    <v-list>
      <template v-for="item in searchRes">
        <v-list-tile :key="item" @click="">
          <v-list-tile-content>
            <v-list-tile-title>{{item}}</v-list-tile-title>
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
export default {
  name: 'Draw',
  data() {
    return {
      drawer: true,
      searchStr: "",
      apis: ["adam's", "mad", "aces", "add", "subtract", "mult", "matmul", "dot"],
      searchRes: ["adam's", "mad", "aces", "add", "subtract", "mult", "matmul", "dot"]
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
    },
    filterSearchResults() {
      this.searchRes = this.apis.filter(this.searchMatch);
    },
    searchMatch(str) {
      return str.search(this.searchStr) !== -1;
    }
  }
}
</script>

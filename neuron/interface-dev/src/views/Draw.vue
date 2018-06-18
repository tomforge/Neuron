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
    <svg id="board" width=1280 height=720 fill="white"></svg>
</div>
</template>
<script>
import * as d3 from "d3";
import * as dagreD3 from "dagre-d3"
export default {
  name: 'Draw',
  data() {
    return {
      drawer: true,
      graph: "",
      searchStr: "",
      apis: ["adam's", "mad", "aces", "add", "subtract", "mult", "matmul", "dot"],
      searchRes: ["adam's", "mad", "aces", "add", "subtract", "mult", "matmul", "dot"]
    }
  },
  mounted() {
    this.initDagreD3Graph();

    let g = this.graph;

    g.setNode("a", {label: "a"});
    g.setNode("b", {label: "b"});
    g.setEdge("a", "b", {label: "a to b"});

    // Create the renderer
    var render = new dagreD3.render();

    // Set up an SVG group so that we can translate the final graph.
    var svg = d3.select("svg"),
        svgGroup = svg.append("g");

    // Set up zoom support
    var zoom = d3.zoom().on("zoom", function() {
          svgGroup.attr("transform", d3.event.transform);
        });
    svg.call(zoom);

    // Run the renderer. This is what draws the final graph.
    render(svgGroup, g);

    // Center the graph
    var initialScale = 0.75;
    svg.call(zoom.transform, d3.zoomIdentity.translate((svg.attr("width") - g.graph().width * initialScale) / 2, 20).scale(initialScale));

    svg.attr('height', g.graph().height * initialScale + 40);;
    
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
    },
    initDagreD3Graph() {
      this.graph = new dagreD3.graphlib.Graph()
          .setGraph({})
          .setDefaultEdgeLabel(function() { return {}; });
    }
  }
}
</script>

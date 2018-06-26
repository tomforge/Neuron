<template>
    <v-container fluid fill-height>
        <!-- LEFT DRAWER -->
        <v-navigation-drawer v-model="drawer" class="pa-0 noscroll left-pane-style" clipped app permanent>
            <v-layout column fill-height>
                <v-flex>
                    <v-tabs slider-color="grey darken-4">
                        <div class="attr-selection" style="width: 100%; height:100%">
                        <v-tab active-class="grey darken-3">Add Nodes</v-tab>
                        <v-tab active-class="grey darken-3">LOREM</v-tab>
                        <v-tab active-class="grey darken-3">IPSUM</v-tab>
                        </div>
                    </v-tabs>
                </v-flex>
                <v-flex class="panel-style" style="min-height:0" xs8>
                    <v-card id="nodes-panel" height="100%">
                        <v-layout column fill-height>
                            <v-flex class="shrink">
                                <!-- Search bar -->
                                <v-text-field class="px-3 pb-0 pt-1 body-1" :append-icon-cb="() => {}" placeholder="Search nodes" single-line
                                              append-icon="search" color="white" hide-details
                                              v-model="searchStr"></v-text-field>
                            </v-flex>
                            <!-- Node list -->
                            <v-flex class="scroll">
                                <v-list>
                                    <template v-for="item in filteredNodeTypes">
                                        <v-menu :key="item.id"
                                                open-on-hover
                                                open-delay="200"
                                                close-delay="0"
                                                right
                                                offset-x
                                                full-width
                                                :close-on-content-click="false">
                                            <!-- Node list item -->
                                            <v-list-tile slot="activator" @click="" color="grey lighten-1">
                                                <v-list-tile-content>
                                                    <v-list-tile-title class="text-xs-center body-2"
                                                            v-html="$options.filters.highlight(item.name, searchStr, 'white')">
                                                        {{item.name}}
                                                    </v-list-tile-title>
                                                </v-list-tile-content>
                                            </v-list-tile>
                                            <!--Doc viewer popup-->
                                            <v-card class="scroll" flat color="grey darken-2" height="500px">
                                                <v-card-title>
                                                    <span class="headline">{{item.name}}</span>
                                                </v-card-title>
                                                <v-card-text>
                                                    <!--TODO: better formatting for docs-->
                                                    <pre>{{item.doc}}</pre>
                                                </v-card-text>
                                            </v-card>
                                        </v-menu>
                                    </template>
                                </v-list>
                            </v-flex>
                        </v-layout>
                    </v-card>
                </v-flex>

                <!-- Attributes panel -->
                <v-flex class="panel-style" style="min-height:0" xs4>
                    <v-card height="100%" class="elevation-5 grey--text text--lighten-2">
                        <v-layout column fill-height>
                            <!-- Selection title -->
                            <v-flex class="shrink">
                                <v-card-title class="justify-center subheading pa-1 attr-selection">
                                    <b>Selection:</b>&nbsp <em style="color:#F4FF81">{{Object.keys(selectedNode).length === 0 ? 'NIL' : selectedNode.name}}</em>
                                </v-card-title>
                            </v-flex>
                            <!-- Attributes list -->
                            <v-flex class="scroll">
                                <v-data-table :items="selectedNode.attr" hide-actions hide-headers>
                                    <template slot="items" slot-scope="props">
                                        <tr id="attr-row">
                                            <!-- Attribute name -->
                                            <th class="text-xs-center"> {{props.item.name | titleCase}}</th>
                                            <td class="pa-0">:</td>
                                            <!-- Attribute value -->
                                            <td width="100%">
                                                <v-edit-dialog :return-value.sync="props.item.value" lazy>
                                                    <!-- Value display -->
                                                    <span class="text-xs-center">{{props.item.value}}</span>
                                                    <!-- Value edit display -->
                                                    <v-text-field slot="input" v-model="props.item.value"
                                                                  label="Edit" single-line></v-text-field>
                                                </v-edit-dialog>
                                            </td>
                                        </tr>
                                    </template>
                                </v-data-table>
                            </v-flex>
                        </v-layout>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-navigation-drawer>
        <!-- MAIN BOARD -->
        <svg id="board" style="width: 100%; height: 100%; overflow:visible"></svg>
    </v-container>
</template>

<style scoped>
.noscroll {
  overflow: hidden;
}

.scroll {
  overflow: auto;
}
.scroll::-webkit-scrollbar {
  width: 6px;
  background-color: #6d6867;
}
.scroll::-webkit-scrollbar-thumb {
  background-color: #2d2d2d;
  border-radius: 15px;
}
.scroll::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #6d6867;
  border-radius: 15px;
}
.panel-style {
  border-top: hidden;
  border-left: 4px inset #212121;
  border-right: 4px inset #212121;
  border-bottom: 4px inset #212121;
  border-radius: 10px;
}
.left-pane-style {
  border-top: hidden;
  border-left: hidden;
  border-right: 4px solid #191919;
  border-bottom: hidden;
  border-radius: 5px;
}
/* No inbuilt way to change data-table color, so override bg-color manually. */
#attr-row {
  background-color: #3c3c3c;
  color: #e0e0e0;
}

/* Hover color is lost when bg-color is manually set. Need to enable it */
#attr-row:hover {
  background-color: #424242;
}
.attr-selection {
  background-color: #2d2d2d;
}
</style>

<script>
import * as d3 from "d3";
import * as dagreD3 from "dagre-d3";
import { mapState } from "vuex";

export default {
  name: "Draw",
  data() {
    return {
      drawer: true,
      graph: "",
      nodes: [],
      edges: [],
      searchStr: "",
      selectedNode: {
        name: "Adam's Mad Aces",
        attr: [
          {
            name: "Name",
            value: "lorem"
          },
          {
            name: "Filters",
            value: "3"
          },
          {
            name: "Activity Regularizer",
            value: "dolor"
          },
          {
            name: "kernel regularizer",
            value: "sit"
          },
          {
            name: "kernel initializer",
            value: "amet"
          },
          {
            name: "bias constraint",
            value: "consectectur"
          },
          {
            name: "trainable",
            value: "true"
          },
          {
            name: "data format",
            value: "hello"
          }
        ]
      }
    };
  },
  computed: {
    // vuex state
    ...mapState({
      nodeTypes: "nodeTypes",
      wsConnected: "wsConnected"
    }),

    filteredNodeTypes() {
      if (!this.searchStr) {
        return this.nodeTypes;
      } else {
        return this.nodeTypes.filter(
          // Return only word-boundary matches (e.g. don't return "add" if
          // searching for "d")
          nodeType => nodeType.name.search("\\b" + this.searchStr) !== -1
        );
      }
    }
  },
  mounted() {
    if (!this.nodeTypes.length) {
      this.$store.commit("emit", ["API_get_node_meta", ""]);
    }

    this.initDagreD3Graph();

    let g = this.graph;

    /* Generate array of nodes and edges */
    let numNodes = 10,
      numEdges = numNodes;
    for (let n = 0; n < numNodes; n++) {
      this.nodes.push({
        name: n
      });
    }
    for (let e = 0; e < numEdges - 1; e++) {
      this.edges.push({
        from: e,
        to: (e + 1) % numEdges,
        name: e + " to " + ((e + 1) % numEdges)
      });
    }
    this.addNodes(this.nodes);
    this.addEdges(this.edges);

    // g.setNode("a", {label: "a"});
    // g.setNode("b", {label: "b"});
    // g.setEdge("a", "b", {label: "a to b"});

    // Create the renderer
    let render = new dagreD3.render();

    // Set up an SVG group so that we can translate the final graph.
    let svg = d3.select("svg"),
      svgGroup = svg.append("g");

    // Set up zoom support
    let zoom = d3.zoom().on("zoom", function() {
      svgGroup.attr("transform", d3.event.transform);
    });
    svg.call(zoom);

    /* This D3 dragging code doesn't seem to work for individual node*/
    // svg.selectAll("circle")
    //     .call(d3.drag()
    //         .on("start", dragstarted)
    //         .on("drag", dragged)
    //         .on("end", dragended));

    // function dragstarted(d) {
    //   d3.select(this).raise().classed("active", true);
    // }

    // function dragged(d) {
    //   d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
    // }

    // function dragended(d) {
    //   d3.select(this).classed("active", false);
    // }

    // Run the renderer. This is what draws the final graph.
    render(svgGroup, g);

    // Center the graph
    let initialScale = 0.75;
    svg.call(
      zoom.transform,
      d3.zoomIdentity
        .translate((svg.attr("width") - g.graph().width * initialScale) / 2, 20)
        .scale(initialScale)
    );

    // svg.attr('height', g.graph().height * initialScale + 40);
  },
  methods: {
    initDagreD3Graph() {
      this.graph = new dagreD3.graphlib.Graph()
        .setGraph({
          nodesep: 30,
          ranksep: 150,
          rankdir: "LR",
          marginx: 20,
          marginy: 20
        })
        .setDefaultEdgeLabel(function() {
          return {};
        });
    },
    addNode(node) {
      this.graph.setNode(node.name, {
        shape: "circle",
        label: node.name,
        labelStyle: "fill: #000000",
        style: "fill: #FFFFFF"
      });
    },
    addEdge(edge) {
      this.graph.setEdge(edge.from, edge.to, {
        label: edge.name,
        labelStyle: "fill: #FFFFFF",
        style: "stroke: #f66; stroke-width: 3px;",
        arrowheadStyle: "fill: #f66"
      });
    },
    addNodes(nodes) {
      let self = this;
      nodes.forEach(function(node) {
        self.addNode(node);
      });
    },
    addEdges(edges) {
      let self = this;
      edges.forEach(function(edge) {
        self.addEdge(edge);
      });
    }
  },

  filters: {
    highlight: function(str, toMatch, color) {
      let matcher = new RegExp(toMatch, "i");
      return str.replace(
        matcher,
        matched => '<span style="color:' + color + '">' + matched + "</span>"
      );
    },
    titleCase: function(str) {
      if (!str) return "";
      return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    }
  }
};
</script>

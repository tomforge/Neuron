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
                                <v-text-field class="px-3 pb-0 pt-1 body-1" :append-icon-cb="() => {}"
                                              placeholder="Search nodes" single-line
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
                                    <b>Selection:</b>&nbsp; <em style="color:#F4FF81">{{Object.keys(selectedNode).length
                                    === 0 ? 'NIL' : selectedNode.name}}</em>
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
        <svg>
            <g/>
        </svg>
        <v-btn v-on:click.native="addNode">Add Node</v-btn>
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
      nodeCounter: 1,
      searchStr: "",
      selectedNode: {}
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
    this.graphEditor();
  },
  methods: {
    graphEditor() {
      function initGraph() {
        return new dagreD3.graphlib.Graph().setGraph({
          nodesep: 30,
          ranksep: 150,
          rankdir: "LR",
          marginx: 20,
          marginy: 20
        });
      }
      // Initialize graph
      this.graph = initGraph();
      let g = this.graph;
      let self = this;

      /* not using this for now */
      // let data_updates = {
      //   nodes: [],
      //   edges: []
      // }

      function updateGraph() {
        // Preparation of DagreD3 data structures
        g = initGraph();
        resetMouseVars();

        self.nodes.sort();
        // Add nodes
        self.nodes.forEach(function(node) {
          if (node.type == "host") {
            g.setNode(node.name, {
              labelType: "html",
              label: node.name,
              class: "host",
              rx: 5,
              ry: 5,
              width: 150
            });
          } else {
            g.setNode(node.name, {
              labelType: "html",
              label: node.name,
              class: "comp",
              rx: 5,
              ry: 5,
              width: 150
            });
          }
        });

        // Add edges
        self.edges.forEach(function(edge) {
          let edgeclass = "normal";
          // if (edge.source == 'comp_d') {
          //     edgeclass = "warning";
          // }
          g.setEdge(edge.source, edge.target, {
            label: "",
            labelStyle: "fill: #FFFFFF",
            arrowhead: "vee",
            arrowheadStyle: "fill: #a5a5a5",
            style: "stroke: #a5a5a5; stroke-dasharray: 5, 5;",
            lineInterpolate: "bundle"
          });
        });
        _updateGraph();
      }

      // mouse event vars
      let selected_node = null,
        selected_link = null,
        mousedown_link = null,
        mousedown_node = null,
        mouseup_node = null,
        md_node = null,
        md_node_x = null,
        md_node_y = null,
        hide_line = true,
        pre_scale = null;

      function resetMouseVars() {
        mousedown_node = null;
        mouseup_node = null;
        mousedown_link = null;
        md_node_x = null;
        md_node_y = null;
        hide_line = true;
        pre_scale = null;
      }

      function _updateGraph() {
        let render = new dagreD3.render();
        // Set graph height and init zoom
        let svg = d3.select("svg");
        let container = svg.select("g");

        render(container, g);

        // Set up zoom support
        // let zoom = d3.zoom()
        //     .on('zoom', function() {
        //       container.attr("transform", d3.event.transform);
        //     });
        // svg.call(zoom);

        // define arrow markers for graph links
        function edgeArrowMarkerStyle(svg) {
          svg
            .append("svg:defs")
            .append("svg:marker")
            .attr("id", "end-arrow")
            .attr("viewBox", "0 0 10 10")
            .attr("refX", 9)
            .attr("refY", 5)
            .attr("markerUnits", "strokeWidth")
            .attr("markerWidth", 8)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M 0 0 L 10 5 L 0 10 L 4 5 z")
            .style("stroke-width", 4)
            .style("stroke-dasharray", "1,0")
            .attr("fill", "#a5a5a5");

          let defs = d3.select("svg").selectAll("defs");
          let filter = defs
            .append("filter")
            .attr("id", "drop_shadow")
            .attr("height", "130%");
          filter
            .append("feGaussianBlur")
            .attr("in", "SourceAlpha")
            .attr("stdDeviation", 5)
            .attr("result", "blur");
          filter
            .append("feOffset")
            .attr("in", "blur")
            .attr("dx", 2)
            .attr("dy", 2)
            .attr("result", "offsetBlur");
          let cpec_light = filter
            .append("feSpecularLighting")
            .attr("in", "blur")
            .attr("surfaceScale", "5")
            .attr("specularConstant", "0.75")
            .attr("specularExponent", "20")
            .attr("lighting-color", "#73A0D1")
            .attr("result", "specOut");
          cpec_light
            .append("fePointLight")
            .attr("x", "-5000")
            .attr("y", "-10000")
            .attr("z", "20000");
          filter
            .append("feComposite")
            .attr("in", "specOut")
            .attr("in2", "SourceAlpha")
            .attr("operator", "in")
            .attr("result", "specOut");
          filter
            .append("feComposite")
            .attr("in", "SourceGraphic")
            .attr("in2", "specOut")
            .attr("operator", "arithmetic")
            .attr("k1", "0")
            .attr("k2", "1")
            .attr("k3", "1")
            .attr("k4", "0")
            .attr("result", "litPaint");
          filter
            .append("feOffset")
            .attr("in", "litPaint")
            .attr("dx", -4)
            .attr("dy", -4)
            .attr("result", "litPaint");
          let feMerge = filter.append("feMerge");
          feMerge.append("feMergeNode").attr("in", "offsetBlur");
          feMerge.append("feMergeNode").attr("in", "litPaint");

          // let feMerge = filter.append("feMerge");
          // feMerge.append("feMergeNode")
          //       .attr("in", "offsetBlur");
          // feMerge.append("feMergeNode")
          //       .attr("in", "SourceGraphic");
        }
        edgeArrowMarkerStyle(svg);

        // Handle mouse events for nodes
        d3.selectAll("svg g.node")
          .on("mouseover", function(d) {
            if (!mousedown_node || d === mousedown_node) return;
            if (!pre_scale) {
              pre_scale = d3.select(this).attr("transform");
              d3.select(this).attr("transform", pre_scale + " scale(1.2)");
            }
          })
          .on("mouseout", function(d) {
            if (!mousedown_node) return;
            if (pre_scale) {
              d3.select(this).attr("transform", pre_scale);
              pre_scale = null;
            }
            if (d === mousedown_node) {
              hide_line = false;
            }
          })
          .on("mousedown", function(d) {
            // d3.event.stopPropagation();
            svg.on('.zoom', null);
            console.log('node mousedown');

            mousedown_node = d;

            // Retrieve node using node's name
            md_node = g.node(d);
            md_node_x = md_node.x + md_node.width / 2;
            md_node_y = md_node.y;

            /* This line doesn't do anything if I'm not wrong */
            drag_line
              .style("marker-end", "url(#end-arrow)")
              .attr(
                "d",
                "M" +
                  md_node_x +
                  "," +
                  md_node_y +
                  "L" +
                  md_node_x +
                  "," +
                  md_node_y
              );
          })
          .on("mouseup", function(d) {
            if (!mousedown_node) return;
            svg.call(zoom);

            // needed by FF
            drag_line.classed("hidden", true).style("marker-end", "");

            // check for drag-to-self
            mouseup_node = d;
            if (mouseup_node === mousedown_node) {
              // select node
              if (mouseup_node !== selected_node) {
                selected_node = mouseup_node;
                self.selectedNode = self.nodes.filter(
                  node => node.name === selected_node
                )[0];
              }
              selected_link = null;
              resetMouseVars();
              return;
            }

            //Check if there is already an existing edge between mouseup and mousedown nodes
            let existing_edge = g.edge(mousedown_node, mouseup_node);
            if (!existing_edge) {
              g.setEdge(mousedown_node, mouseup_node, {
                label: "",
                labelStyle: "fill: #FFFFFF",
                arrowhead: "vee",
                arrowheadStyle: "fill: #a5a5a5",
                style: "stroke: #a5a5a5; stroke-dasharray: 5, 5;",
                lineInterpolate: "bundle"
              });
              self.edges.push({
                source: mousedown_node,
                target: mouseup_node
              });
            }
            _updateGraph();
          });

        // Handle mouse events for edges
        d3.selectAll(".edgePath, .edgeLabel")
          .on("mouseover", function(d) {
            let dClass = d3.select(this).attr("class");
            if (dClass === "edgeLabel") {
              if (!pre_scale) {
                pre_scale = d3.select(this).attr("transform");
                d3.select(this).attr("transform", pre_scale + " scale(1.2)");
              }
            } else if (dClass === "edgePath") {
              d3.select(this)
                .select('.path')
                .transition()
                .duration(25)
                .style('stroke-width', '8');
            }
          })
          .on("mouseout", function(d) {
            let dClass = d3.select(this).attr("class");
            if (dClass === "edgeLabel") {
              if (pre_scale) {
                d3.select(this).attr("transform", pre_scale);
                pre_scale = null;
              }
            } else {
              d3.select(this)
                .select('.path')
                .transition()
                .duration(50)
                .style('stroke-width', '4');
            }            
          })
          .on("click", function(d) {
            console.log("clicked edge: " + JSON.stringify(g.edge(d)));
            mousedown_link = d;
            if (mousedown_link !== selected_link) {
              selected_link = mousedown_link;
            }
            selected_node = null;
          });

        // Handle keypress events in body element (as SVG elements cannot detect keypress)
        d3.select("body").on("keydown", function() {
          if (d3.event.keyCode === 46) {
            // console.log("node to delete: " + selected_node);
            // console.log("edge to delete: " + JSON.stringify(selected_link));
            if (selected_node) {
              self.nodes = self.nodes.filter(function(n) {
                return n.name !== selected_node;
              });
              self.edges = self.edges.filter(function(e) {
                return e.source !== selected_node && e.target !== selected_node;
              });
              selected_node = null;
            } else if (selected_link) {
              self.edges = self.edges.filter(function(e) {
                return (
                  e.source !== selected_link.v || e.target !== selected_link.w
                );
              });
              selected_link = null;
            }
            console.log("nodes: " + JSON.stringify(self.nodes));
            console.log("edges: " + JSON.stringify(self.edges));
            updateGraph();
          }
        });
      }

      updateGraph();

      function mousemove() {
        // console.log('svg mousemove, mousedown_node=' + mousedown_node + ', hide_line ' +hide_line);
        if (!mousedown_node) return;
        drag_line
          .classed("hidden", hide_line)
          .attr(
            "d",
            "M" +
              (md_node_x + zoomTrans.x) * zoomTrans.scale +
              "," +
              (md_node_y + zoomTrans.y) * zoomTrans.scale +
              "L" +
              d3.mouse(this)[0] +
              "," +
              d3.mouse(this)[1]
          );
      }

      function mouseup() {
        // console.log('svg mouseup');
        if (mousedown_node) {
          // hide drag line
          drag_line.classed("hidden", true).style("marker-end", "");
        }

        // because :active only works in WebKit?
        svg.classed("active", false);

        // clear mouse event vars
        resetMouseVars();
      }

      let svg = d3.select("svg");
      // line displayed when dragging new edges
      let drag_line = svg
        .append("svg:path")
        .attr("class", "link dragline hidden")
        .attr("marker-mid", "")
        .attr("d", "M0,0L0,0");

      let zoomTrans = {
        x: 0,
        y: 0,
        scale: 1
      }

      let zoom = d3.zoom()
        .scaleExtent([1, Infinity])
        .on('zoom', function() {
          zoomTrans.x = d3.event.transform.x;
          zoomTrans.y = d3.event.transform.y;
          zoomTrans.scale = d3.event.transform.k;
          svg.select('g').attr("transform", d3.event.transform);
        })

      svg.call(zoom);
      svg.on("mousemove", mousemove)
        .on("mouseup", mouseup);

      // let drag = d3.drag().on('drag', function(d) {
      //   svg.attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
      // })
    },
    addNode() {
      this.nodes.push({
        type: "host",
        name: "node" + this.nodeCounter++,
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
      });
      this.graphEditor(); // re-render after adding node
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

<!-- Styles for drawing board. Dynamic content styles don't work with style scoped.
 https://github.com/vuejs/vue-loader/issues/559 -->
<style>
svg {
  /* idk why the height can't use 100% */
  height: 100%;
  width: 100%;
  overflow: visible;
}

.node.comp rect {
  fill: #2378ce;
  width: 200px;
}

.node:hover {
  filter: url(#drop_shadow);
}

.node.comp.ext rect {
  fill: #2378ce;
  width: 444px;
}

.node.comp.new rect {
  fill: #76ace2;
  width: 200px;
}

.node.host rect {
  fill: #239ddb;
  width: 150px;
}

.node g div {
  fill: #239ddb;
  width: 150px;
  height: 48px;
}

.node .ext g div {
  fill: #239ddb;
  width: 250px;
  height: 48px;
}

.node g div img {
  width: 48px;
  height: 48px;
}

.edgeLabel rect {
  fill: #f45;
}

.edgePath path.path {
  stroke-width: 4px;
  fill: none;
}

.edgePath path.path .new {
  stroke: #a5a5a5;
}

.edgePath {
  stroke: black;
  stroke-width: 0px;
}

.edgePath off {
  stroke: red;
  stroke-width: 0px;
}

.edge:hover {
  stroke: #353940;
  stroke-width: 6px;
}

.edge .normal {
  stroke: black;
  fill: black;
}

.edge .new {
  stroke: #a5a5a5;
  fill: #a5a5a5;
}

.edge .warning {
  stroke: red;
  fill: red;
}

/* This styles the title of the tooltip */
.tipsy .name {
  font-size: 1.5em;
  font-weight: bold;
  color: #60b1fc;
  margin: 0;
}

/* This styles the body of the tooltip */
.tipsy .description {
  font-size: 1.2em;
}

.d3-context-menu {
  position: absolute;
  display: none;
  background-color: #f2f2f2;
  border-radius: 4px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  min-width: 150px;
  border: 1px solid #d4d4d4;
  z-index: 1200;
}

.d3-context-menu ul {
  list-style-type: none;
  margin: 4px 0px;
  padding: 0px;
  cursor: default;
}

.d3-context-menu ul li {
  padding: 4px 16px;
}

.d3-context-menu ul li:hover {
  background-color: #4677f8;
  color: #fefefe;
}

path.link {
  fill: none;
  stroke: #a5a5a5;
  stroke-width: 4px;
  stroke-dasharray: 10, 2;
  cursor: default;
}

svg:not(.active):not(.ctrl) path.link {
  cursor: pointer;
}

path.link.selected {
  stroke-dasharray: 10, 2;
}

path.link.dragline {
  pointer-events: none;
}

path.link.hidden {
  stroke-width: 0;
}
</style>

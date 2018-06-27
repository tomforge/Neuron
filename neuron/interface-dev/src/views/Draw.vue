<template>
<v-container fluid fill-height>
  <!-- LEFT DRAWER -->
  <v-navigation-drawer v-model="drawer" clipped app permanent>
    <v-text-field class="pa-2" :append-icon-cb="() => {}" placeholder="Search" single-line append-icon="search" color="white" hide-details v-model="searchStr"></v-text-field>
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
  <div class="container">
    <svg><g/></svg>
  </div>
  <v-btn v-on:click.native="addNode">Add Node</v-btn>
</v-container>
</template>
<script>
import * as d3 from "d3";
import * as dagreD3 from "dagre-d3"
import {
  mapState
} from "vuex";
export default {
  name: 'Draw',
  data() {
    return {
      drawer: true,
      graph: "",
      nodes: [],
      edges: [],
      nodeCounter: 1,
      searchStr: "",
    }
  },
  computed: {
    // vuex state
    ...mapState({
      nodeTypes: "nodeTypes"
    }),

    filteredNodeTypes() {
      if (!this.searchStr) {
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
      // var data_updates = {
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
            var edgeclass = "normal";
            // if (edge.source == 'comp_d') {
            //     edgeclass = "warning";
            // }
            g.setEdge(edge.source, edge.target,
              {
                label: "",
                labelStyle: "fill: #FFFFFF",
                arrowhead: "vee",
                arrowheadStyle: "fill: #a5a5a5",
                style: "stroke: #a5a5a5; stroke-dasharray: 5, 5;",
                lineInterpolate: 'bundle'
              });
        });
        _updateGraph();
      }

      // mouse event vars
      var selected_node = null,
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
        var render = new dagreD3.render();
        // Set graph height and init zoom
        var svg = d3.select("svg");
        var container = svg.select("g");

        render(container, g);

        // Set up zoom support
        // let zoom = d3.zoom()
        //     .on('zoom', function() {
        //       container.attr("transform", d3.event.transform);
        //     });
        // svg.call(zoom);
        
        
        // define arrow markers for graph links
        function edgeArrowMarkerStyle(svg) {
              svg.append('svg:defs').append('svg:marker')
                  .attr('id', 'end-arrow')
                  .attr("viewBox", "0 0 10 10")
                  .attr("refX", 9)
                  .attr("refY", 5)
                  .attr("markerUnits", "strokeWidth")
                  .attr("markerWidth", 8)
                  .attr("markerHeight", 6)
                  .attr("orient", "auto")
                .append('svg:path')
                  .attr('d', 'M 0 0 L 10 5 L 0 10 L 4 5 z')
                  .style("stroke-width", 1)
                  .style("stroke-dasharray", "1,0")
                  .attr('fill', '#a5a5a5');
              
              var defs = d3.select('svg').selectAll('defs');
              var filter = defs.append('filter')
                  .attr('id', 'drop_shadow')
                  .attr('height', '130%');
              filter.append("feGaussianBlur")
                    .attr("in", "SourceAlpha")
                    .attr("stdDeviation", 5)
                    .attr("result", "blur");
              filter.append("feOffset")
                    .attr("in", "blur")
                    .attr("dx", 2)
                    .attr("dy", 2)
                    .attr("result", "offsetBlur");
              var cpec_light = filter.append('feSpecularLighting')
                .attr('in', 'blur')
                .attr('surfaceScale', '5')
                .attr('specularConstant', '0.75')
                .attr('specularExponent', '20')
                .attr('lighting-color', '#73A0D1')
                .attr('result', 'specOut');
              cpec_light.append('fePointLight')
                .attr('x', '-5000')
                .attr('y', '-10000')
                .attr('z', '20000');
              filter.append('feComposite')
                .attr('in', 'specOut')
                .attr('in2', 'SourceAlpha')
                .attr('operator', 'in')
                .attr('result', 'specOut');
              filter.append('feComposite')
                .attr('in', 'SourceGraphic')
                .attr('in2', 'specOut')
                .attr('operator', 'arithmetic')
                .attr('k1', '0')
                .attr('k2', '1')
                .attr('k3', '1')
                .attr('k4', '0')
                .attr('result', 'litPaint');
              filter.append("feOffset")
                    .attr("in", "litPaint")
                    .attr("dx", -4)
                    .attr("dy", -4)
                    .attr("result", "litPaint");
              var feMerge = filter.append("feMerge");
              feMerge.append("feMergeNode")
                    .attr("in", "offsetBlur");
              feMerge.append("feMergeNode")
                    .attr("in", "litPaint");
              
              // var feMerge = filter.append("feMerge");
              // feMerge.append("feMergeNode")
              //       .attr("in", "offsetBlur");
              // feMerge.append("feMergeNode")
              //       .attr("in", "SourceGraphic");
        }
        edgeArrowMarkerStyle(svg);
        
        // Handle mouse events for nodes
        d3.selectAll('svg g.node')
        .on('mouseover', function (d) {
          if(!mousedown_node || d === mousedown_node) return;
          if (!pre_scale) {
            pre_scale = d3.select(this).attr('transform');
            d3.select(this).attr('transform', pre_scale + ' scale(1.2)');    
          }
        })
        .on('mouseout', function(d) {
          if (!mousedown_node) return;
          if (pre_scale) {
            d3.select(this).attr('transform', pre_scale);
            pre_scale = null;
          }
          if (d === mousedown_node) {
            hide_line = false;
          }
        })
        .on('mousedown', function(d) {
          mousedown_node = d;

          // Retrieve node using node's name
          md_node = g.node(d);
          md_node_x = md_node.x + (md_node.width/2);
          md_node_y = md_node.y;
          // console.log(md_node);

          /* This line doesn't do anything if I'm not wrong */
          drag_line
            .style('marker-end', 'url(#end-arrow)')
            .attr('d', 'M' + md_node_x + ',' + md_node_y + 'L' + md_node_x + ',' + md_node_y);
        })
        .on('mouseup', function(d) {
          if(!mousedown_node) return;

          // needed by FF
          drag_line
            .classed('hidden', true)
            .style('marker-end', '');

          // check for drag-to-self
          mouseup_node = d;
          if(mouseup_node === mousedown_node) {
            // select node
            if(mouseup_node === selected_node) {
              selected_node = null;
            } else {
              selected_node = mouseup_node;
            } 
            selected_link = null;
            resetMouseVars();
            return;
          }

          //Check if there is already an existing edge between mouseup and mousedown nodes
          var existing_edge = g.edge(mousedown_node, mouseup_node);
          if (!existing_edge) {
            g.setEdge(mousedown_node, mouseup_node, {
                        label: "",
                        labelStyle: "fill: #FFFFFF",
                        arrowhead: "vee",
                        arrowheadStyle: "fill: #a5a5a5",
                        style: "stroke: #a5a5a5; stroke-dasharray: 5, 5;",
                        lineInterpolate: 'bundle' 
                        });
            self.edges.push({
              "source": mousedown_node,
              "target": mouseup_node
            })
          } 
          _updateGraph();
        });

        // Handle mouse events for edges
        d3.selectAll('.edgePath, .edgeLabel')
        .on('mouseover', function (d) {
          // console.log(d);
          let dClass = d3.select(this).attr('class');
          // console.log(dClass);
          if (dClass === 'edgeLabel') {
            if (!pre_scale) {
              pre_scale = d3.select(this).attr('transform');
              d3.select(this).attr('transform', pre_scale + ' scale(1.2)');    
            }
          } else if (dClass === 'edgePath') {
            // doesnt work yet
            d3.select(this).attr('stroke-width', '2px');
          }
        })
        .on('mouseout', function(d) {
          if (pre_scale) {
            d3.select(this).attr('transform', pre_scale);
            pre_scale = null;
          }
        })
        .on('click', function(d) {
          console.log('clicked edge')
          mousedown_link = d;
          if (mousedown_link === selected_link) {
            selected_link = null;
          } else {
            selected_link = mousedown_link;
          }
          selected_node = null;
        });

        // Handle keypress events in body element (as SVG elements cannot detect keypress)
        d3.select('body')
        .on('keydown', function() { 
          if (d3.event.keyCode === 46) {
            console.log("node to delete: " + selected_node);
            console.log("edge to delete: " + JSON.stringify(selected_link));
            if (selected_node) {
              self.nodes = self.nodes.filter(function(n) {
                return n.name !== selected_node;
              });
              self.edges = self.edges.filter(function(e) {
                return e.source !== selected_node 
                  && e.target !== selected_node;
              })
              selected_node = null;
            } else if (selected_link) {
              self.edges = self.edges.filter(function(e) {
                return e.source !== selected_link.v  
                  && e.target !== selected_link.w;
              });
              selected_link = null;
            }
            console.log('nodes: ' + JSON.stringify(self.nodes));
            console.log('edges: ' + JSON.stringify(self.edges));
            updateGraph();
          }
        });
      }

      updateGraph();

      // For reason unknown this empty function is required to be here or nothing will work
      function mousedown() {
      }

      function mousemove() {
        // console.log('svg mousemove, mousedown_node=' + mousedown_node + ', hide_line ' +hide_line);
        if(!mousedown_node) return;

        drag_line
          .classed('hidden', hide_line)
          .attr('d', 'M' + md_node_x + ',' + md_node_y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);
        
      }

      function mouseup() {
        // console.log('svg mouseup');
        if(mousedown_node) {
          // hide drag line
        drag_line
            .classed('hidden', true)
            .style('marker-end', '');
        }

        // because :active only works in WebKit?
        svg.classed('active', false);

        // clear mouse event vars
        resetMouseVars();
      }

      var svg = d3.select("svg");
      // line displayed when dragging new nodes
      var drag_line = svg.append('svg:path')
        .attr('class', 'link dragline hidden')
        .attr("marker-mid", "")
        .attr('d', 'M0,0L0,0');
        
      svg.on('mousedown', mousedown)
        .on('mousemove', mousemove)
        .on('mouseup', mouseup);

    },
    addNode() {
      this.nodes.push({
        type: "host",
        name: "node" + this.nodeCounter++
      });
      this.graphEditor(); // re-render after adding node
    },
  },

  filters: {
    highlight: function(str, toMatch, color) {
      let matcher = new RegExp(toMatch, "i");
      return str.replace(matcher,
        matched => ("<span style=\"color:" + color + "\">" + matched + "</span>"));
    }
  }
}
</script>
<style>
  svg{
    /* idk why the height can't use 100% */
    height: 1920px;
    width: 100%;
    overflow: "visible";
  }

  .node.comp rect {
    fill: #2378CE;
    width: 200px;
  }
  .node:hover {
    filter: url(#drop_shadow);
  }
  .node.comp.ext rect {
    fill: #2378CE;
    width: 444px;
  }

  .node.comp.new rect {
    fill: #76ACE2;
    width: 200px;
  }

  .node.host rect {
    fill: #239DDB; 
    width: 150px;
  }

  .node g div {
    fill: #239DDB; 
    width: 150px;
    height: 48px;
  }

  .node .ext g div {
    fill: #239DDB; 
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
    stroke-width: 2px;
    fill: none;
  }

  .edgePath path.path .new{
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
  z-index:1200;
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
    stroke-dasharray: 10,2;
    cursor: default;
  }

  svg:not(.active):not(.ctrl) path.link {
    cursor: pointer;
  }

  path.link.selected {
    stroke-dasharray: 10,2;
  }

  path.link.dragline {
    pointer-events: none;
  }

  path.link.hidden {
    stroke-width: 0;
}

</style>
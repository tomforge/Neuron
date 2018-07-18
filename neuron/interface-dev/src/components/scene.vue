<template>
    <svg>
        <g></g>
    </svg>
</template>

<script>
import * as d3 from "d3";
import * as dagreD3 from "dagre-d3";
import { mapState } from "vuex";

export default {
  name: "scene",
  computed: {
    // vuex state
    ...mapState({
      nodes: "nodes",
      edges: "edges"
    })
  },
  data() {
    return {
      rendered_graph: "",
      svg_selection: null,
      g_selection: null,
      drag_line_selection: null,
      zoom: null,
      zoomTrans: {
        x: 0,
        y: 0,
        scale: 1
      },
      nodeCounter: 0,
      selected_node_id: null,
      selected_link: null,
      md_node_id: null,
      md_node: null,
      md_node_x: null,
      md_node_y: null,
      hide_line: true,
      ctrlDown: false,
      shiftDown: false
    };
  },
  mounted() {
    this.svg_selection = d3.select("svg");
    this.g_selection = this.svg_selection.select("g");

    // init line displayed when dragging new edges
    this.drag_line_selection = this.svg_selection
      .append("svg:path")
      .attr("class", "link dragline hidden")
      .attr("marker-mid", "")
      .attr("d", "M0,0L0,0");

    // Init zoom events
    this.zoom = d3
      .zoom()
      .scaleExtent([0, Infinity])
      .on("zoom", () => {
        this.zoomTrans.x = d3.event.transform.x;
        this.zoomTrans.y = d3.event.transform.y;
        this.zoomTrans.scale = d3.event.transform.k;
        this.g_selection.attr("transform", d3.event.transform);
      });

    this.setSVGMouseEvents();
    this.setKeyEvents();

    this.svg_selection.call(this.zoom);
    this.refreshGraph();

    this.$store.watch(
      // The only operations are addition and removal, so we only
      // need to track the length of the two arrays. Multiply edges by
      // prime number to ensure uniqueness
      state => state.nodes.length + 17 * state.edges.length,
      this.refreshGraph
    );
  },
  methods: {
    initGraph() {
      this.rendered_graph = new dagreD3.graphlib.Graph().setGraph({
        nodesep: 30,
        ranksep: 150,
        rankdir: "LR",
        marginx: 20,
        marginy: 20
      });
    },
    refreshNodesInRendering() {
      this.nodes.forEach(node => {
        this.rendered_graph.setNode(node.name, {
          labelType: "html",
          label: node.name,
          class: "comp",
          rx: 5,
          ry: 5,
          width: 150
        });
      });
    },
    refreshEdgesInRendering() {
      this.edges.forEach(edge => {
        this.rendered_graph.setEdge(edge.source, edge.target, {
          label: "",
          labelStyle: "fill: #FFFFFF",
          arrowhead: "vee",
          arrowheadStyle: "fill: #a5a5a5",
          style: "stroke: #a5a5a5;",
          lineInterpolate: "bundle"
        });
      });
    },
    setEdgeArrowMarkerStyle() {
      this.svg_selection
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

      let filter = d3
        .select("svg")
        .selectAll("defs")
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
    },
    setNodeMouseEvents() {
      // Handle mouse events for nodes
      d3.selectAll("svg g.node")
        .on("mouseover", function(d) {
          //TODO: Highlight on hover
        })
        .on("mouseout", d => {
          if (this.md_node_id === d) {
            this.hide_line = false;
          }
        })
        .on("mousedown", d => {
          // Disable zoom
          this.svg_selection.on(".zoom", null);
          console.log("node mousedown");

          this.md_node_id = d;
          // Retrieve rendered node using node's id
          this.md_node = this.rendered_graph.node(d);
          this.md_node_x = this.md_node.x + this.md_node.width / 2;
          this.md_node_y = this.md_node.y;

          this.drag_line_selection
              .style("marker-end", "url(#end-arrow)")
              .attr(
                "d",
                "M" +
                  this.md_node_x +
                  "," +
                  this.md_node_y +
                  "L" +
                  this.md_node_x +
                  "," +
                  this.md_node_y
              );
        })
        .on("mouseup", d => {
          if (!this.md_node_id) return;
          // Re-enable zoom
          this.svg_selection.call(this.zoom);
          // needed by FF
          this.drag_line_selection
            .classed("hidden", true)
            .style("marker-end", "");
          // check for drag-to-self (i.e. click)
          if (this.md_node_id === d) {
            // select node
            if (this.selected_node_id !== d) {
              this.selected_node_id = d;
              this.$store.commit("selectNodeById", d);
            }
            this.selected_link = null;
          } else {
            //Check if there is an existing edge between mousedown and mouseup nodes
            let existing_edge = this.rendered_graph.edge(this.md_node_id, d);
            if (!existing_edge) {
              this.$store.commit("addEdge", {
                source: this.md_node_id,
                target: d
              });
            }
            this.refreshGraph();
          }
          this.resetMouseVars();
        });
    },
    setEdgeMouseEvents() {
      d3.selectAll(".edgePath, .edgeLabel")
        .on("mouseover", function(d) {
          let dClass = d3.select(this).attr("class"); // TODO: All these "this" here?
          if (dClass === "edgePath") {
            d3.select(this)
              .select(".path")
              .transition()
              .duration(25)
              .style("stroke-width", "8");
          }
        })
        .on("mouseout", function(d) {
          let dClass = d3.select(this).attr("class"); // TODO: "this" here?
          if (dClass !== "edgeLabel") {
            d3.select(this)
              .select(".path")
              .transition()
              .duration(50)
              .style("stroke-width", "4");
          }
        })
        .on("click", d => {
          console.log("clicked edge: " + JSON.stringify(this.rendered_graph.edge(d)));
          if (d !== this.selected_link) {
            this.selected_link = d;
          }
          // Deselect node
          this.selected_node_id = null;
          this.$store.commit("selectNodeById", null);
        });
    },
    setSVGMouseEvents() {
      let self = this;
      this.svg_selection
        .on("mousemove", function() {
          // console.log('svg mousemove, md_node_id=' + md_node_id + ', hide_line ' +hide_line);
          if (self.md_node_id) {
            self.drag_line_selection.classed("hidden", self.hide_line).attr(
              "d",
              "M" +
              (self.md_node_x + self.zoomTrans.x) * self.zoomTrans.scale +
              "," +
              (self.md_node_y + self.zoomTrans.y) * self.zoomTrans.scale +
              "L" +
              d3.mouse(this)[0] + // TODO: what is this "this" referring to???
                "," +
                d3.mouse(this)[1]
            );
          }
        })
        .on("mouseup", () => {
          // console.log('svg mouseup');
          // Re-enable zoom
          this.svg_selection.call(this.zoom);
          
          if (this.md_node_id) {
            // TODO: just set self.hide_line = false?
            // hide drag line
            this.drag_line_selection
              .classed("hidden", true)
              .style("marker-end", "");
          }
          // because :active only works in WebKit?
          this.svg_selection.classed("active", false);
          // clear mouse event vars
          this.resetMouseVars();
        });
    },
    setKeyEvents() {
      // Handle key-press events in body element (as SVG elements cannot detect them)
      d3.select("body")
        .on("keydown", () => {
          switch (d3.event.keyCode) {
            // DEL
            case 46:
              if (this.selected_node_id) {
                this.$store.commit("removeNodeGivenId", this.selected_node_id);
                this.$store.commit("selectNodeById", null);
              } else if (this.selected_link) {
                this.$store.commit("removeEdge", this.selected_link);
              }
              this.refreshGraph();
              break;
            // CTRL
            case 17:
              this.ctrlDown = true;
              break;
            // SHIFT
            case 16:
              this.shiftDown = true;
              break;
            // Z
            case 90:
              if (this.ctrlDown && this.shiftDown) {
                // CTRL+SHIFT+Z
                this.$store.commit("redoGraph");
              } else if (this.ctrlDown) {
                // CTRL + Z
                this.$store.commit("undoGraph");
              }
              break;
          }
        })
        .on("keyup", () => {
          switch (d3.event.keyCode) {
            // CTRL
            case 17:
              this.ctrlDown = false;
              break;
            // SHIFT
            case 16:
              this.shiftDown = false;
              break;
          }
        });
    },
    resetMouseVars() {
      this.md_node_id = null;
      this.md_node_x = null;
      this.md_node_y = null;
      this.hide_line = true;
    },
    refreshGraph() {
      // Preparation of DagreD3 data structures
      this.initGraph();
      this.resetMouseVars();
      this.refreshNodesInRendering();
      this.refreshEdgesInRendering();
      // Create the renderer
      let render = new dagreD3.render();
      render(this.g_selection, this.rendered_graph);

      // define arrow markers for graph links
      this.setEdgeArrowMarkerStyle();
      this.setNodeMouseEvents();
      this.setEdgeMouseEvents();
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

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
                                        <v-menu :key="item.type"
                                                open-on-hover
                                                open-delay="200"
                                                close-delay="0"
                                                right
                                                offset-x
                                                full-width
                                                :close-on-content-click="false">
                                            <!-- Node list item -->
                                            <v-list-tile slot="activator" @click="addNode(item)" color="grey lighten-1">
                                                <v-list-tile-content>
                                                    <v-list-tile-title class="text-xs-center body-2"
                                                                       v-html="$options.filters.highlight(item.type, searchStr, 'white')">
                                                        {{item.type}}
                                                    </v-list-tile-title>
                                                </v-list-tile-content>
                                            </v-list-tile>
                                            <!--Doc viewer popup-->
                                            <v-card class="scroll" flat color="grey darken-2" height="400px" width="300px">
                                                <v-card-title>
                                                    <span class="title">{{item.type}}</span>
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
                                    <em style="color:#F4FF81" v-if="selectedNode !== null">{{selectedNode.type}}</em>
                                    <!-- Leave a space if no selected node-->
                                    <span v-if="selectedNode === null">&nbsp;</span>
                                </v-card-title>
                            </v-flex>
                            <!-- Attributes list -->
                            <v-flex class="scroll">
                                <v-data-table :items="selectedNode === null ? [] : Object.entries(selectedNode.params)" hide-actions hide-headers>
                                    <template slot="items" slot-scope="props">
                                        <tr id="attr-row">
                                            <!-- Attribute name -->
                                            <th class="text-xs-center"> {{props.item[0] | titleCase}}</th>
                                            <td class="pa-0">:</td>
                                            <!-- Attribute value -->
                                            <td width="100%">
                                                <v-edit-dialog :return-value.sync="selectedNode.params[props.item[0]]" lazy>
                                                    <!-- Value display -->
                                                    <span class="text-xs-center">{{props.item[1]}}</span>
                                                    <!-- Value edit display -->
                                                    <v-text-field slot="input" v-model="selectedNode.params[props.item[0]]"
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
        <scene></scene>
        <!-- <v-btn v-on:click.native="addNode">Add Node</v-btn> -->
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
import { mapState } from "vuex";
import scene from "../components/scene";

export default {
  name: "Draw",
  components: {
    scene
  },
  data() {
    return {
      drawer: true,
      nodeCounter: 0,
      searchStr: ""
    };
  },
  computed: {
    // vuex state
    ...mapState({
      nodeTypes: "nodeTypes",
      wsConnected: "wsConnected",
      selectedNode: "selectedNode"
    }),

    filteredNodeTypes() {
      if (!this.searchStr) {
        return this.nodeTypes;
      } else {
        return this.nodeTypes.filter(
          // Return only word-boundary matches (e.g. don't return "add" if
          // searching for "d")
          nodeType =>
            nodeType.type.search(new RegExp("\\b" + this.searchStr, "i")) !== -1
        );
      }
    }
  },
  mounted() {
    if (!this.nodeTypes.length) {
      this.$store.commit("emit", ["API_get_node_meta", ""]);
    }
  },
  methods: {
    addNode(node_type) {
      this.$store.commit("addNode", {
        id: ++this.nodeCounter,
        type: node_type.type,
        name: node_type.type + "<br/> ID: " + this.nodeCounter,
        params: node_type.params
      });
      console.log("added a node");
      console.log(this.$store.state.nodes);
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

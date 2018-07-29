<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs4>
        <h1>Run page</h1>
        <!-- <v-btn v-on:click.native ="triggerClick" >Upload training data</v-btn>
        <input type="file" webkitdirectory @change="onFileChange" ref="inputButton"> -->
        <v-text-field 
          :value="trainingData.label" 
          label="Select training data folder from below"
          append-icon="fa-upload"
          :append-icon-cb="run"
          box
          outline 
          readonly></v-text-field>
        <TreeView 
          :model="model" 
          :display="display" 
          :category="category"
          :selection="selection"
          :onSelect="onSelect"
          :search="search"
          :sort="sort"
          :transition="transition"
          :strategies="strategies"
          ></TreeView>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { TreeView } from "@bosket/vue";
import { string } from "@bosket/tools";

export default {
  name: "Run",
  components: {
    TreeView: TreeView
  },
  model: {
    prop: "selection",
    event: "selectionChange"
  },
  data() {
    return {
      trainingData: "",
      selection: [],
      model: [
        {
          label: "Directory 1. Has 2 children.",
          items: [
            {
              label: "D1 Child 1. Has 1 children.",
              items: [{ label: "D1C1 Child 1." }]
            },
            { label: "D1 Child 2" }
          ]
        },
        { label: "Directory 2" },
        {
          label: "Directory 3. Has 1 child.",
          items: [{ label: "D3 Child 1" }]
        }
      ],
      category: "items",
      transition: {
        attrs: { appear: true },
        props: { name: "TreeViewTransition" }
      },
      strategies: {
        // Select on click
        click: ["select"],
        // Use keyboard modifiers
        selection: ["modifiers"],
        // Use the opener to control element folding
        fold: ["opener-control"]
      }
    };
  },
  methods: {
    // triggerClick() {
    //   // I'm using a vuetify-button so I need to trigger the JS input button click
    //   // event upon clicking the vueitfy-button. The JS input button is actually
    //   // hidden in the style portion.
    //   this.$refs.inputButton.click();
    // },
    // onFileChange(e) {
    //   var files = e.target.files || e.dataTransfer.files;
    //   if (!files.length)
    //     return;
    //   this.localSelection = files[0];
    //   this.trainingData = this.localSelection;
    // },
    display(item) {
      return <a>{item.label}</a>;
    },
    onSelect(selection) {
      if (!selection[0] || !selection[0].items) {
        return;
      }
      this.selection = selection;
      this.trainingData = selection[0];
      console.log(this.trainingData.label);
      this.$emit("selectionChange", selection);
    },
    search(input) {
      return item => string(item.label).contains(input);
    },
    sort(a, b) {
      return a.label.localeCompare(b.label);
    },
    run() {
      // Use the training data here
      console.log("Training model now...");
    }
  }
};
</script>

<style>
/* input {
    visibility: hidden;
  } */
/* Search bar */

.TreeView > input[type="search"] {
  width: 100%;
  background: rgba(0, 0, 0, 0.05);
  height: 3em;
  border-width: 2px;
  transition: border 0.5s;
}

/* Elements */

.TreeView {
  box-shadow: 0px 0px 10px #dadada;
  white-space: nowrap;
}

.TreeView ul {
  list-style: none;
}

.TreeView li {
  min-width: 100px;
  transition: all 0.25s ease-in-out;
}

.TreeView ul li a {
  color: #ffffff;
}

.TreeView ul li > .item > a {
  display: inline-block;
  vertical-align: middle;
  width: calc(100% - 55px);
  margin-right: 30px;
  padding: 10px 5px;
  text-decoration: none;
  transition: all 0.25s;
}

.TreeView ul li:not(.disabled) {
  cursor: pointer;
}

.TreeView ul li.selected > .item > a {
  color: crimson;
}

.TreeView ul li.selected > .item > a:hover {
  color: #aaa;
}

.TreeView ul li:not(.disabled) > .item > a:hover {
  color: #e26f6f;
}

/* Root elements */

.TreeView ul.depth-0 {
  padding: 20px;
  margin: 0;
  background-color: rgba(255, 255, 255, 0);
  user-select: none;
  transition: all 0.25s;
}

/* Categories : Nodes with children */

.TreeView li.category > .item {
  display: block;
  margin-bottom: 5px;
  transition: all 0.25s ease-in-out;
}

.TreeView li.category:not(.folded) > .item {
  border-bottom: 1px solid crimson;
}

/* Category opener */

.TreeView .opener {
  display: inline-block;
  vertical-align: middle;
  font-size: 20px;
  cursor: pointer;
}

.TreeView .opener::after {
  content: "+";
  display: block;
  transition: all 0.25s;
  font-family: monospace;
}

.TreeView li.category.async > .item > .opener::after {
  content: "!";
}

.TreeView .opener:hover {
  color: #e26f6f;
}

.TreeView li.category:not(.folded) > .item > .opener::after {
  color: crimson;
  transform: rotate(45deg);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.TreeView li.category.loading > .item > .opener::after {
  animation: spin 1s infinite;
}

/* Animations on fold / unfold */

.TreeViewTransition-enter,
.TreeViewTransition-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

.TreeViewTransition-enter-active,
.TreeViewTransition-leave-active {
  transition: all 0.3s ease-in-out;
}
</style>

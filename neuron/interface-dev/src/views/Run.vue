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

import "./TreeView.css"

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
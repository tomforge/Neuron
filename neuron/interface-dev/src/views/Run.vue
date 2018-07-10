<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex shrink>
        <h1>Run page</h1>
        <v-btn v-on:click.native ="triggerClick" >Upload training data</v-btn>
        <input type="file" @change="onFileChange" ref="inputButton">
        <v-text-field :value="trainingData.name" outline readonly></v-text-field>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: "Run",
    data() {
      return {
        trainingData: ""
      }
    },
    methods: {
      triggerClick() { 
        // I'm using a vuetify-button so I need to trigger the JS input button click
        // event upon clicking the vueitfy-button. The JS input button is actually
        // hidden in the style portion.
        this.$refs.inputButton.click();
      },
      onFileChange(e) {
        var files = e.target.files || e.dataTransfer.files;
        if (!files.length)
          return;
        this.trainingData = files[0];
      }
    }
  }
</script>

<style scoped>
  input {
    visibility: hidden;
  }
</style>
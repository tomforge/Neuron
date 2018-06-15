<template>
  <div id="app">
    <img src="./assets/logo.png">
    <Menu msg="Welcome to Your Vue.js App"/>
    <nav>
      <router-link to="/">Menu</router-link>
      <router-link to="/view1">View1</router-link>
      <router-link to="/view2">View2</router-link>      
    </nav>
    <router-view/>
  </div>
</template>

<script>
import Menu from './components/Menu.vue'

export default {
  name: 'app',
  components: {
    Menu
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

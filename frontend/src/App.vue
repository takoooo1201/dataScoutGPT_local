<!-- <template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style> -->
<template>
  <div id="app">
    <h1>Vue Frontend with Flask Backend</h1>
    <button @click="fetchData">Fetch Data</button>
    <p>{{ message }}</p>
    <!-- <router-view></router-view> -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/data');
        this.message = response.data.message;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
};
</script>

<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div id="example-1">
      <button v-on:click="">Add 1</button>
    </div>
  </div>
</template>

<script>
const electron = require('electron')
const ipcRenderer = electron.ipcRenderer
const loadBalancer = require('electron-load-balancer')

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },

  mounted() {

      loadBalancer.start( ipcRenderer ,'interface');
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

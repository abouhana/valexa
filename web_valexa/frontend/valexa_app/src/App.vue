<template>
  <div id="app">
    <file-upload 
      url="http://127.0.0.1:5000/valexa/compute/"
      v-on:fileupload-success="updatePloter($event)">
    </file-upload>
    <profile-ploter v-bind:ploterData="ploterData"></profile-ploter>
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue'
import ProfilePloter from './components/ProfilePloter.vue'

export default {
  name: 'app',
  data() {
    return {
      ploterData: [],
    }
  },
  components: {
    FileUpload,
    ProfilePloter,
  },
  methods: {
    updatePloter(event){
      var data = event.data
      if (!data) {
          alert("No data");
      } else {
        this.ploterData = data.profiles;
      }
    }
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
  /* margin-top: 60px; */
}
</style>

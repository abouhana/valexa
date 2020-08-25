<template>
  <v-row>
      <v-col>
          <Plotly
              :data="graphData.data"
              :layout="graphData.layout"
              :display-mode-bar="false"
          />
      </v-col>
    </v-row>
</template>

<script>
  import { Plotly } from 'vue-plotly'

  export default {
    name: "GraphProfile",
    props: {
      graphData: Object
    },
    components: {
      Plotly
    }
  }
</script>

<style scoped>

</style>
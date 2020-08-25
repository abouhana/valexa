<template>
  <v-row>
    <v-col>
      <Plotly
          :data="graphsData.linearity.data"
          :layout="graphsData.linearity.layout"
          :display-mode-bar="false"
      />
    </v-col>
    <v-col v-if="hasCorrection">
      <Plotly
          :data="graphsData.correction.data"
          :layout="graphsData.correction.layout"
          :display-mode-bar="false"
      />
    </v-col>
  </v-row>
</template>

<script>
  import { Plotly } from 'vue-plotly'

  export default {
    name: "GraphLinearity",
    props: {
      hasCorrection: Boolean,
      graphsData: Object
    },
    components: {
      Plotly
    }
  }
</script>

<style scoped>

</style>
<template>
  <v-row>
    <v-col>
      <Plotly
          :data="residualsData.data"
          :layout="residualsData.layout"
          :display-mode-bar="false"
      />
    </v-col>
    <v-col>
      <Plotly
          :data="residualsStudentData.data"
          :layout="residualsStudentData.layout"
          :display-mode-bar="false"
      />
    </v-col>
  </v-row>
</template>

<script>
  import { Plotly } from 'vue-plotly'

  export default {
    name: "GraphResiduals",
    components: {
      Plotly
    },
    props: {
      residualsData: Object,
      residualsStudentData: Object
    }
  }
</script>

<style scoped>

</style>
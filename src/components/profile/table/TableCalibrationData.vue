<template>
  <v-row>
    <v-col>
      <span class="text-h5">Calibration Data</span>
      <v-data-table
        dense
        :headers="headers"
        :items="tableData"
        class="elevation-1"
        hide-default-footer
        :items-per-page=1000
      >
      </v-data-table>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    name: "TableCalibrationData",
    props: {
      tableData: Array
    },
    computed: {
      headers: function () {
        var header = [
          {text: 'Series', value: 'Series'},
          {text: 'Level', value: 'Level'},
          {text: 'X', value: 'x'},
          {text: 'Y', value: 'y'},
        ]
        return header
      },
    }
  }
</script>

<style scoped>

</style>
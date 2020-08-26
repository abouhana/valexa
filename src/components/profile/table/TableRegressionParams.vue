<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col>
          <span class="text-h5">Calibration Regression</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-data-table
              :headers="headers"
              :items="items"
              dense
              class="elevation-1"
              hide-default-footer
              :items-per-page=1000
          />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    name: "TableRegressionParams",
    props: {
      tableData: Object
    },
    computed: {
      items: function () {
        var itemsArray = []
        this.tableData.regression_info.forEach((value, index) => {
          itemsArray[index] = {index: index, ...value}
        })
        return itemsArray
      }
    },
    data: () => ({
      headers: [
        {
          text: 'Series',
          value: 'index'
        },
        {
          text: 'Equation',
          value: 'function_string'
        },
        {
          text: 'R²',
          value: 'rsquared'
        }
      ]
    })
  }
</script>

<style scoped>

</style>
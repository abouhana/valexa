<template>
      <v-row>
        <v-col>
          <span class="text-h5">Precision and repeatability</span>
          <v-data-table
            dense
            :headers="headers"
            :items="items"
            class="elevation-1"
            hide-default-footer
            :items-per-page=1000
          />
        </v-col>
      </v-row>
</template>

<script>
  export default {
    name: "TableValidationPrecision",
    props: {
      tableData: Object
    },
    computed: {
      items: function() {
        var itemsArray = []
        this.tableData.levels_info.forEach((value, index) => {
          itemsArray[index] = {index: index, ...value}
        })
        this.tableData.intermediate_precision.forEach((value, index) => {
          itemsArray[index] = {...itemsArray[index], ...value}
        })
        this.tableData.repeatability_info.forEach((value, index) => {
          itemsArray[index] = {...itemsArray[index], ...value}
        })
        this.tableData.misc_stats.forEach((value, index) => {
          itemsArray[index] = {...itemsArray[index], ...value}
        })
        return itemsArray
      }
    },
    data: () => ({
      headers: [
        {
          text: 'Level',
          value: 'index'
        },
        {
          text: 'Introduced Concentration',
          value: 'introduced_concentration'
        },
        {
          text: 'Absolute Intermediate Precision',
          value: 'intermediate_precision_std'
        },
        {
          text: 'Relative Intermediate Precision',
          value: 'intermediate_precision_cv'
        },
        {
          text: 'Absolute Repeatability',
          value: 'repeatability_std'
        },
        {
          text: 'Relative Repeatability',
          value: 'repeatability_cv'
        },
        {
          text: 'Variance ratio',
          value: 'ratio_var'
        }
      ]
    })
  }
</script>

<style scoped>

</style>
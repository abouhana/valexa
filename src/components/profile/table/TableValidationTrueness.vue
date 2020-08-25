<template>
      <v-row>
        <v-col>
          <span class="text-h5">Trueness</span>
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
    name: "TableValidationTrueness",
    props: {
      tableData: Object
    },
    computed: {
      items: function() {
        var itemsArray = []
        this.tableData.levels_info.forEach((value, index) => {
          itemsArray[index] = {index: index, ...value}
        })
        this.tableData.bias_info.forEach((value, index) => {
          itemsArray[index] = {...itemsArray[index], ...value}
        })
        this.tableData.tolerance_info.forEach((value, index) => {
          itemsArray[index] = {...itemsArray[index], ...value}
        })
        itemsArray.forEach((value, index, array) => {
          array[index] = {
            ...value,
            tolerance_abs: value.tolerance_abs_high + ', ' + value.tolerance_abs_low,
            tolerance_rel: value.tolerance_rel_high + ', ' + value.tolerance_rel_low
          }
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
          text: 'Calculated Concentration',
          value: 'calculated_concentration'
        },
        {
          text: 'Absolute Bias',
          value: 'bias_abs'
        },
        {
          text: 'Relative Bias (%)',
          value: 'bias_rel'
        },
        {
          text: 'Recovery (%)',
          value: 'recovery'
        },
        {
          text: 'Tolerance Absolute',
          value: 'tolerance_abs'
        },
        {
          text: 'Tolerance Relative (%)',
          value: 'tolerance_rel'
        }
      ]
    })
  }
</script>

<style scoped>

</style>
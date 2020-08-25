<template>
  <v-row>
    <v-col>
      <v-simple-table
        dense
      >
        <thead>
          <tr>
            <th class="text-left">Parameter</th>
            <th class="text-left">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Slope</td>
            <td>{{linearityData.slope.value}}</td>
          </tr>
          <tr>
            <td>Intercept</td>
            <td>{{linearityData.intercept.value}}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-col>
    <v-col v-if="hasCorrection">
      <v-simple-table
          dense
      >
        <thead>
          <tr>
            <th class="text-left">Parameter</th>
            <th class="text-left">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Slope</td>
            <td>{{correctionData.slope.value}}</td>
          </tr>
          <tr>
            <td>Intercept</td>
            <td>{{correctionData.intercept.value}}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    name: "TableRegressionParams"
  }
</script>

<style scoped>

</style>
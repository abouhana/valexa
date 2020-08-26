<template>
  <v-row>
    <v-col>
      <v-simple-table
        dense
        class="elevation-1"
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
          <tr>
            <td>R²</td>
            <td>{{linearityData.rsquared.value}}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-col>
    <v-col v-if="hasCorrection">
      <v-simple-table
          dense
          class="elevation-1"
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
          <tr>
            <td>R²</td>
            <td>{{correctionData.rsquared.value}}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    name: "TableLinearity",
    props: {
      hasCorrection: Boolean,
      linearityData: Object,
      correctionData: Object
    }
  }
</script>

<style scoped>

</style>
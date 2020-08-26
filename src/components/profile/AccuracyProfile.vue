<template>
  <div>
    <TableValidationSummary :table-data="profileData.model_info"/>
    <GraphProfile :graph-data="profileData.graphs.profile"/>
    <TableValidationTrueness :table-data="profileData"/>
    <TableValidationPrecision :table-data="profileData"/>
    <TableValidationUncertainty :table-data="profileData"/>
    <GraphLinearity
        v-if="profileData.regression_info.length > 0"
        :graphs-data="profileData.graphs"
        :has-correction="profileData.model_info.has_correction"
        :table-data="profileData"
    />
    <TableValidationData :table-data="profileData.validation_data"/>
    <span v-if="profileData.regression_info.length > 0">
      <v-divider dark></v-divider>
      <TableRegressionParams :table-data="profileData"/>
      <GraphRegression :graph-data="profileData.graphs.regression"/>
      <GraphResiduals
          :residuals-data="profileData.graphs.residuals"
          :residuals-student-data="profileData.graphs.residuals_std"
      />
      <TableCalibrationData :table-data="profileData.calibration_data"/>
    </span>
  </div>
</template>

<script>
    import { mapGetters } from "vuex"
    import TableValidationData from "./table/TableValidationData";
    import TableValidationSummary from "./table/TableValidationSummary";
    import GraphProfile from "./table/GraphProfile";
    import GraphLinearity from "./table/GraphLinearity";
    import GraphRegression from "./table/GraphRegression";
    import TableLinearity from "./table/TableLinearity";
    import GraphResiduals from "./table/GraphResiduals";
    import TableValidationTrueness from "./table/TableValidationTrueness";
    import TableValidationPrecision from "./table/TableValidationPrecision";
    import TableValidationUncertainty from "./table/TableValidationUncertainty";
    import TableRegressionParams from "./table/TableRegressionParams";
    import TableCalibrationData from "./table/TableCalibrationData";

    export default {
        components: {
          TableCalibrationData,
          TableRegressionParams,
          TableValidationUncertainty,
          TableValidationPrecision,
          TableValidationTrueness,
          GraphResiduals,
          TableLinearity,
          GraphRegression,
          GraphLinearity,
          GraphProfile,
          TableValidationSummary,
          TableValidationData,
        },

        props: {
            xAxeString: String,
            yAxeString: String,
            profileId: Number,
            absoluteAcceptance: Boolean,
            compoundName: String
        },

        computed: {

            ...mapGetters([
               'getProfile'
            ]),

            profileData: function () {
                return this.getProfile({id: this.profileId, compoundName: this.compoundName})
            },
        },
        mounted: function () {
          console.log(this.profileData.regression_info.length)
        }
    }


</script>

<style scoped>

</style>
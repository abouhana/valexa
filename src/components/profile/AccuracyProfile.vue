<template>
  <div>
    <TableValidationSummary :table-data="profileData.model_info"/>
    <GraphProfile :graph-data="profileData.graphs.profile"/>
    <TableValidationTrueness :table-data="profileData"/>
    <TableValidationPrecision :table-data="profileData"/>
    <TableValidationData :table-data="profileData.validation_data"/>
    <v-divider dark></v-divider>
    <GraphLinearity :graphs-data="profileData.graphs" :has-correction="profileData.model_info.has_correction"/>
    <TableLinearity v-if="profileData.model_info.has_correction"
        :linearity-data="profileData.linearity_info"
        :has-correction="profileData.model_info.has_correction"
        :correction-data="profileData.correction_info"
    />
    <TableLinearity v-else
        :linearity-data="profileData.linearity_info"
        :has-correction="profileData.model_info.has_correction"
    />
    <GraphRegression :graph-data="profileData.graphs.regression"/>
    <GraphResiduals
        :residuals-data="profileData.graphs.residuals"
        :residuals-student-data="profileData.graphs.residuals_std"
    />

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

    export default {
        components: {
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

        data () {
            return {

            }
        }
    }


</script>

<style scoped>

</style>
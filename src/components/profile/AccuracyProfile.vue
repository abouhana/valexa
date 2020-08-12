<template>
    <div>
      <v-row>
        <v-col>
          <v-simple-table
            dense>
              <thead>
                <tr>
                  <th class="text-left">Parameter</th>
                  <th class="text-left">Value</th>
                </tr>
              </thead>
            <tbody>
              <tr>
                <td>LOD</td>
                <td>{{profileData.model_info.lod}} {{profileData.model_info.units}} ({{profileData.model_info.lod_type}})</td>
              </tr>
              <tr>
                <td>LOQ Min</td>
                <td>{{profileData.model_info.min_loq}} {{profileData.model_info.units}}</td>
              </tr>
              <tr>
                <td>LOQ Max</td>
                <td>{{profileData.model_info.max_loq}} {{profileData.model_info.units}}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-col>
        <v-col>
          <v-simple-table
              dense>
            <thead>
              <tr>
                <th class="text-left">Parameter</th>
                <th class="text-left">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Correction</td>
                <td>
                  <span v-if="profileData.model_info.has_correction">{{profileData.model_info.correction_factor}}
                    <span v-if="profileData.model_info.forced_correction_value>0">(Forced)</span>
                  </span>
                  <span v-else>---</span>
                </td>
              </tr>
              <tr>
                <td>Average Recovery</td>
                <td>{{profileData.model_info.average_recovery}}</td>
              </tr>
              <tr>
                <td>Tolerance</td>
                <td>{{profileData.model_info.tolerance}} %</td>
              </tr>
              <tr>
                <td>Acceptance</td>
                <td>
                  {{profileData.model_info.acceptance}}
                  <span v-if="profileData.model_info.absolute_acceptance">(Absolute)</span>
                  <span v-else>(Relative)</span>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
            <Plotly
                :data="profileData.graphs.profile.data"
                :layout="profileData.graphs.profile.layout"
                :display-mode-bar="false"
            />
        </v-col>
      </v-row>
      <TableValidationData :table-data="profileData.validation_data"/>
      <v-row>
        <v-col>
          <Plotly
              :data="profileData.graphs.linearity.data"
              :layout="profileData.graphs.linearity.layout"
              :display-mode-bar="false"
          />
        </v-col>
        <v-col v-if="profileData.model_info.has_correction">
          <Plotly
              :data="profileData.graphs.correction.data"
              :layout="profileData.graphs.correction.layout"
              :display-mode-bar="false"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <Plotly
              :data="profileData.graphs.regression.data"
              :layout="profileData.graphs.regression.layout"
              :display-mode-bar="false"
          />
        </v-col>
      </v-row>
    </div>
</template>

<script>
    import { Plotly } from 'vue-plotly'
    import { mapGetters } from "vuex"
    import TableValidationData from "./table/TableValidationData";

    export default {
        components: {
          TableValidationData,
          Plotly
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
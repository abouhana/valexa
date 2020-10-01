
<template>
  <v-card class="secondary" shaped elevation="2">
    <v-card-title>Rapport de Validation</v-card-title>
    <v-card-text>
      <v-row>
        <v-col>
          <v-card shaped flat>
            <v-card-title>Informations du rapport</v-card-title>
            <v-card-text>
              <v-list-item two-line v-for="comp in this.profilesReport">
                <v-list-item-content>
                  <v-list-item-title>{{comp.compound_name}}</v-list-item-title>
                  <v-list-item-subtitle>{{comp.model_info.model_name}}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>


          <v-card shaped flat>
            <v-card-title>Informations du rapport</v-card-title>
            <v-card-text>
              coc

            </v-card-text>
          </v-card>





          <v-col>
            <v-checkbox v-model="typeReport" label="Word" value="word"/>
          </v-col>
          <v-col>
            <v-checkbox v-model="typeReport" label="PDF" value="pdf"/>
          </v-col>
          <v-col>
            <v-checkbox v-model="typeReport" label="Tous les fichiers" value="all"/>
          </v-col>
          <v-col>
            <v-checkbox v-model="typeReport" label="Projet TEX" value="tex"/>
          </v-col>

          <v-btn text @click="createReport()" v-bind:disabled="this.beDisable">Génerer le rapport</v-btn>

        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
const electron = require('electron')
const ipcRenderer = electron.ipcRenderer
const loadBalancer = require('electron-load-balancer')

export default {
  name: "ReportView",
  computed: {
    ...mapState(['profilesReport']),
    beDisable: function(){
      return !(this.profilesReport.length > 0 && this.typeReport.length > 0);
    }

  },
  methods: {
    createReport: function(){
      loadBalancer.start(ipcRenderer, 'processProfilesReport')
    },

  },
  mounted() {

    ipcRenderer.on("CHANNEL_PROFILES_REPORT", (event, args) => {  // LISTENER CHANNEL
      console.log("Listener sur CHANNEL_PROFILES_REPORT: "+ JSON.stringify(args).toString())
      if(JSON.stringify(args).toString() === '"processProfilesReport READY"'){  // le process peut recueillir des infos
        loadBalancer.sendData(ipcRenderer, 'processProfilesReport', {data: {profiles: this.profilesReport, typeReport: this.typeReport}})  //TODO: + tex pdf
      }
      if(args.type === "END"){
        loadBalancer.sendData(ipcRenderer, 'processProfilesReport', {data: 'EXIT'})  //stop process
      }

    })

  },
  data: () => ({
    typeReport: []
  })
}
</script>

<style scoped>

</style>
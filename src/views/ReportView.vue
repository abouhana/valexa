
<template>
  <v-card shaped light>
        <v-card-title>Rapport</v-card-title>
        <v-card-text>
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
      ...mapState(['profilesReport'])
    },
    mounted() {
      if(this.profilesReport.length > 0){  // rapport contient des informations
        loadBalancer.start(ipcRenderer, 'processProfilesReport')
      }

      ipcRenderer.on("CHANNEL_PROFILES_REPORT", (event, args) => {
        console.log("Listener sur CHANNEL_PROFILES_REPORT: "+ JSON.stringify(args).toString())

        if(JSON.stringify(args).toString() === '"processProfilesReport READY"'){  // le process peut recueillir des infos
          loadBalancer.sendData(ipcRenderer, 'processProfilesReport', {data: this.profilesReport})
        }

        if(args.type === "END"){
          loadBalancer.sendData(ipcRenderer, 'processProfilesReport', {data: 'EXIT'})  //stop process
        }
      })

    },
    data: () => ({})
  }
</script>

<style scoped>

</style>
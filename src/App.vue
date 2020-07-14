<template>
  <v-app id="inspire">
    <v-navigation-drawer
            v-model="drawer"
            app
            :clipped="$vuetify.breakpoint.lgAndUp"
            color="primary"
    >
      <LeftBar/>
    </v-navigation-drawer>

    <v-app-bar
            app
            dark
            :clipped-left="$vuetify.breakpoint.lgAndUp"
            color="primary darken-3"
    >
      <v-app-bar-nav-icon
              @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-toolbar-title>Valexa</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container
              class="fill-height secondary"
              fluid
      >
        <v-row
                align-content="center"
        >
          <v-col class="text-center">
            <router-view/>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer
            app
            dark
            color="primary darken-3"
    >
      <span class="white--text">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
  import LeftBar from "./components/LeftBar";
  const electron = require('electron')
  const ipcRenderer = electron.ipcRenderer
  const loadBalancer = require('electron-load-balancer')
  import { mapMutations, mapGetters, mapState } from 'vuex'
  export default {
    components: {
      LeftBar
    },
    props: {
      source: String,
    },
    computed: {
      ...mapState([
        'validationAccepted'
      ])
    },
    mounted: function () {
      ipcRenderer.on("GEN_MESSAGE", (event, args) => {
        //console.log(args)
      })
    },
    data: () => ({
      drawer: null,
      pyMessage: ""
    }),
  }
</script>

<style>
  .no-scroll > * {
    overflow-x: hidden !important;
  }
  .v-navigation-drawer {
    z-index: 999999 !important;
  }
</style>
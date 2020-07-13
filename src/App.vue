<template>
    <v-app id="inspire">
        <v-navigation-drawer
          v-model="drawer"
          app
          :clipped="$vuetify.breakpoint.lgAndUp"
          color="primary"
        >
              <v-list dense>
                    <v-list-item link>
                          <v-list-item-action>
                              <v-icon>mdi-home</v-icon>
                          </v-list-item-action>
                          <v-list-item-content>
                              <v-list-item-title>Home</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item link>
                            <v-list-item-action>
                                <v-icon>mdi-email</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>Contact</v-list-item-title>
                            </v-list-item-content>
                    </v-list-item>
              </v-list>
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
                class="fill-height"
                fluid
              >
                    <v-row
                      align="center"
                      justify="center"
                    >
                          <v-col class="text-center">
                                <DataEntry/>
                                <LoadingPage v-if="validationAccepted!==true"/>
                                <ProfileTable v-if="validationAccepted===true"/>
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

    import ValidationProgress from "./components/ValidationProgress";
    import LoadingPage from "./pages/LoadingPage";
    import MainPage from "./pages/MainPage";
    import AccuracyProfile from "./components/profiles/AccuracyProfile";
    import DataEntry from "./pages/DataEntry";
    import ProfileTable from "./pages/ProfileTable";
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')
    import { mapMutations, mapGetters, mapState } from 'vuex'

    export default {
        components: {
            DataEntry,
            LoadingPage,
            ValidationProgress,
            AccuracyProfile,
            MainPage,
            ProfileTable
        },
        props: {
            source: String,
        },
        computed: {
            ...mapState([
                'validationAccepted'

            ])
        },
        mounted () {
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
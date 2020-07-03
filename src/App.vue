<template>
    <v-app id="inspire">
        <v-app-bar
                app
                clipped-right
                color="blue-grey"
                dark
        >
            <v-app-bar-nav-icon v-show="validationAccepted===true" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Valexa</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-navigation-drawer
                v-model="drawer"
                app
        >
            <v-list dense>
            </v-list>
        </v-navigation-drawer>

        <v-main>
            <v-container
                    class="fill-height"
            >
                <v-row
                        justify="center"
                        align="center"
                >
                    <v-col>
                        <DataEntry/>
                        <LoadingPage v-if="validationAccepted!==true"/>
                        <MainPage v-if="validationAccepted!==true"/>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>

        <v-footer
                app
                color="blue-grey"
                class="white--text"
        >
            <span>Vuetify</span>
            <v-spacer></v-spacer>
            <span>{{pyMessage}}</span>
            <v-spacer></v-spacer>
            <span>&copy; 2019</span>
        </v-footer>
    </v-app>
</template>

<script>

    import ValidationProgress from "./components/ValidationProgress";
    import LoadingPage from "./pages/LoadingPage";
    import MainPage from "./pages/MainPage";
    import AccuracyProfile from "./components/profiles/AccuracyProfile";
    import DataEntry from "./pages/DataEntry";
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
            MainPage
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
            drawer: false,
            pyMessage: ""
        }),
    }
</script>

<style>
    .no-scroll > * {
        overflow-x: hidden !important;
    }
</style>
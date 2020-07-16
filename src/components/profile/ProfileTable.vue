<i18n>
    {
    "en": {
        "continue": "Continue"
    },
    "fr": {
        "continue": "Continuer"
    }
}
</i18n>

<template>
    <v-card
            shaped
            light
    >
        <v-card-title>Profiles</v-card-title>
        <v-card-text>
            <v-data-table
                :headers="headers"
                :items="getProfilesTable"
                :expanded.sync="expanded"
                dense
                show-expand
                :loading="stateLoading.profile"
            >
                <template v-slot:expanded-item="{ headers, item }">
                    <td :colspan="headers.length"><AccuracyProfile
                            :profile-id="item.id"
                            x-axe-string="test"
                            y-axe-string="test2"
                    ></AccuracyProfile></td>
                </template>
            </v-data-table>
        </v-card-text>
    </v-card>
</template>

<script>
    import { mapMutations, mapGetters, mapState, mapActions } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')
    import AccuracyProfile from "./AccuracyProfile";

    export default {


        name: "MainPage",
        components: {
            AccuracyProfile,
        },
        methods: {
            ...mapMutations([
                'makeProfileList',
                'setStateLoading',
                'finishListOfProfile'
            ])
        },
        computed: {
            ...mapState([
                'stateLoading',
                'listOfProfileCompleted'
            ]),
            ...mapGetters([
                'getProfilesTable'
            ]),
        },
        mounted() {
            if (!this.listOfProfileCompleted) {

                ipcRenderer.on('PROFILE', (events, args) => {
                    if (args.data === "START") {
                        this.setStateLoading({name: 'profiles', status: true})
                    } else if (args.data === "STOP") {
                        this.setStateLoading({name: 'profiles', status: true})
                        this.finishListOfProfile()
                    } else {
                        this.makeProfileList(args.data)
                    }

                })

                loadBalancer.start(ipcRenderer, 'test')
            }
        },
        data () {
            return {
                finishedLoading: false,
                expanded: [],
                headers: [
                    { text: 'Id', value: 'id' },
                    { text: 'Model', value: 'model_info.model_name' },
                    { text: 'LOD', value: 'model_info.lod' },
                    { text: 'Min LOQ', value: 'model_info.min_loq' },
                    { text: 'Max LOQ', value: 'model_info.max_loq' },
                    { text: '', value: 'data-table-expand' },
                ]
            }
        }
    }
</script>

<style scoped>

</style>
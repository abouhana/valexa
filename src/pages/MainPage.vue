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
    <div>
        <v-data-table
            :headers="headers"
            :items="getProfilesTable"
            :expanded.sync="expanded"
            dense
            show-expand
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length"><AccuracyProfile
                        :profile-id="item.id"
                        x-axe-string="test"
                        y-axe-string="test2"
                ></AccuracyProfile></td>
            </template>
        </v-data-table>
    </div>
</template>

<script>
    import { mapMutations, mapGetters, mapState, mapActions } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')
    import AccuracyProfile from "../components/profiles/AccuracyProfile";
    import LoadingPage from "./LoadingPage";
    import ValidationProgress from "../components/ValidationProgress";

    export default {


        name: "MainPage",
        components: {
            AccuracyProfile,
        },
        methods: {
            ...mapMutations([
                'makeProfileList',
                'setStateLoading'
            ])
        },
        computed: {
            ...mapState([
                'stateLoading',
            ]),
            ...mapGetters([
                'getProfilesTable'
            ]),
        },
        mounted() {
            this.setStateLoading(true)

            ipcRenderer.on('PROFILE', (events, args) => {
                this.makeProfileList(args.data)
                this.setStateLoading(false)
            })

            loadBalancer.start( ipcRenderer ,'test')
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
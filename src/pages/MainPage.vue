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
        <v-data-table>
            :headers="headers"
            :items="getProfilesTable"
        </v-data-table>
    </div>
</template>

<script>
    import { mapMutations, mapGetters, mapState, mapActions } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {


        name: "MainPage",
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
                this.makeProfileList(args)
                this.setStateLoading(false)
                console.log(this.getProfilesTable)
            })

            loadBalancer.start( ipcRenderer ,'test')
        },
        data () {
            return {
                finishedLoading: false,
                headers: [
                    { text: 'Profile', value: 'model_type' },
                ]
            }
        }
    }
</script>

<style scoped>

</style>
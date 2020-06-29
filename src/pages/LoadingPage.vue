<template>
    <div id="loading">
        <v-row
                justify="center"
                align="center"
        >
        <h2>{{ messageShown }}</h2>
        </v-row>
        <v-row
                justify="center"
                align="stretch"
        >
            <div class="view">
                <ValidationProgress v-bind:progress="getValidationProgress"></ValidationProgress>
            </div>
        </v-row>
        <v-row
                justify="center"
                align="start"
        >
            Validating against: {{ validationCurrentName }} <br>
            Pass: {{validationPass}} out of {{ validationTotalNumber }} <br>
            Fail: {{validationFail}} out of {{ validationTotalNumber }}
        </v-row>
    </div>
</template>

<script>
    import ValidationProgress from "../components/ValidationProgress"
    import { mapMutations, mapGetters, mapState } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "LoadingPage",
        components: { ValidationProgress },
        methods: {
            ...mapMutations([
                'incrementValidationFail',
                'incrementValidationPass',
                'incrementValidationCurrentNumber',
                'setValidationTotalNumber',
                'setValidationCurrentName',
                'setValexaIsValidTrue',
                'setValidationStatus',
                'addValidationDescription'
            ])
        },
        computed: {
            ...mapState([
                'valexaIsValid',
                'validationTotalNumber',
                'validationCurrentNumber',
                'validationPass',
                'validationFail',
                'validationCurrentName',
                'validationDescription',
                'validationStatus'
            ]),

            ...mapGetters([
                'getValidationProgress'
            ])
        },
        data () {
            return {
                messageShown: "Please wait",
                currentValidation: "",
                numberOfValidation: 0,
                numberOfFail: 0,
                numberOfPass: 0,
                validationName: ""
            }
        },

        mounted() {
            ipcRenderer.on("VALID_INFO",  (event, args) => {
                this.setValidationTotalNumber(args.numberOfValidation)
                if (args.status === "start") {
                    this.setValidationStatus("start")
                } else if (args.status === "done") {
                    this.setValidationStatus("done")
                }
            })

            ipcRenderer.on("VALID_NAME",  (event, args) => {
                this.setValidationCurrentName(args.validationName)
            })

            ipcRenderer.on("VALID_PASS",  (event, args) => {
                this.incrementValidationPass()
            })

            ipcRenderer.on("VALID_PASS",  (event, args) => {
                this.incrementValidationFail()
            })

            loadBalancer.start( ipcRenderer ,'validate')
        },
    }
</script>

<style scoped>

</style>
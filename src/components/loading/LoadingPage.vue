<i18n>
    {
        "en": {
            "validation": {
                "loading": "Please wait while I load.",
                "started": "I am validating myself",
                "done": "All done!",
                "pass": "Everything looks good :)",
                "fail": "There seems to be a problems :(",
                "article": "I am currently testing myself against:"
            },
            "continue": "Continue"
        },
        "fr": {
            "validation": {
                "loading": "Veuillez patienter pendant que je me charge",
                "started": "Je suis en train de me valider",
                "done": "Fini!",
                "pass": "Tout semble bien :)",
                "fail": "On dirait qu'il y a un problème :(",
                "article": "Je m'évalue présentement selon:"
            },
            "continue": "Continuer"
        }
    }
</i18n>

<template>
    <div id="loading">
        <v-row
                justify="center"
                align="center"
        >
            <h2 v-if="validationStatus === 'start'">{{ $t('validation.started') }}</h2>
            <h2 v-else-if="validationStatus === 'done'">{{ $t('validation.done') }}</h2>
            <h2 v-else>{{ $t('validation.loading') }}</h2>
        </v-row>
        <div v-if="validationStatus !== '' ">
            <div>
                <v-row
                        justify="center"
                >
                    <div class="view">
                        <ValidationProgress v-bind:progress="getValidationProgress"></ValidationProgress>
                    </div>
                </v-row>
            </div>
            <div v-show="validationStatus === 'start'">
                <v-row
                        justify="center"
                        align-content="start"
                        class="text-center"
                >
                    <h3 class="text-center">{{$t('validation.article') }}</h3>
                    <br>
                    {{ validationCurrentName }}
                </v-row>
            </div>
            <div v-if="validationStatus === 'done'">
                <v-row
                        justify="center"
                        align-content="start"
                >
                    <h3 v-if="valexaIsValid === true" class="text-center">{{$t('validation.pass') }}</h3>
                    <h3 v-else class="text-center">{{$t('validation.fail') }}</h3>
                </v-row>
                <v-row>
                    <v-simple-table
                            :dense=true
                            class="no-scroll"
                    >
                        <tr v-for="validation in validationDescription">
                            <td>{{ validation.name }}</td>
                            <td>
                                <v-icon v-if="validation.status === 'pass'" color="green">mdi-check-circle</v-icon>
                                <v-icon v-else color="red">mdi-alert</v-icon>
                            </td>
                        </tr>
                    </v-simple-table>
                </v-row>
                <v-row align-content="center" justify="center">
                    <v-btn color="success" x-large @click="setValidationAccepted()">{{ $t('continue') }}</v-btn>
                </v-row>
            </div>
        </div>
    </div>
</template>

<script>
    import ValidationProgress from "../components/ValidationProgress"
    import { mapMutations, mapGetters, mapState } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "loading-page",
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
                'addValidationDescription',
                'setValidationAccepted',
                'setStateLoading'
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
                'validationStatus',
                'stateLoading'
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
                validationName: "",
            }
        },

        mounted() {
            this.setStateLoading(true)

            ipcRenderer.on("VALID_INFO",  (event, args) => {
                this.setValidationTotalNumber(args.numberOfValidation)
                if (args.status === "start") {
                    this.setValidationStatus("start")
                } else if (args.status === "done") {
                    this.setStateLoading(false)
                    this.setValidationStatus("done")
                    if (this.validationPass === this.validationTotalNumber) {
                        this.setValexaIsValidTrue()
                    }
                }
            })

            ipcRenderer.on("VALID_NAME",  (event, args) => {
                this.setValidationCurrentName(args.validationName)
            })

            ipcRenderer.on("VALID_PASS",  (event, args) => {
                this.incrementValidationCurrentNumber()
                this.incrementValidationPass()
                this.addValidationDescription("pass")
            })

            ipcRenderer.on("VALID_FAIL",  (event, args) => {
                this.incrementValidationCurrentNumber()
                this.incrementValidationFail()
                this.addValidationDescription("fail")
            })

            loadBalancer.start( ipcRenderer ,'validate')
        },
    }
</script>

<style scoped>

</style>
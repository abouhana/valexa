<i18n>
    {
        "en": {
            "validation": {
                "loading": "Please wait while I load.",
                "started": "I am validating myself",
                "done": "All done!",
                "pass": "Everything looks good :)",
                "fail": "There seems to be a problems :(",
                "article": "I am currently testing myself against:",
                "accept": "Accept the verification"
            }
        },
        "fr": {
            "validation": {
                "loading": "Veuillez patienter pendant que je me charge",
                "started": "Je suis en train de me valider",
                "done": "Fini!",
                "pass": "Tout semble bien :)",
                "fail": "On dirait qu'il y a un problème :(",
                "article": "Je m'évalue présentement selon:",
                "accept": "Accepter la vérification"
            }
        }
    }
</i18n>

<template>
    <v-card
            shaped
            light
            :loading="stateLoading"
    >
        <v-card-title>Initialization</v-card-title>
        <v-card-text class="black--text">
            <v-row justify="center">
                    <h2 v-if="validationStatus === 'start'">{{ $t('validation.started') }}</h2>
                    <h2 v-else-if="validationStatus === 'done'">{{ $t('validation.done') }}</h2>
                    <h2 v-else>{{ $t('validation.loading') }}</h2>
            </v-row>
            <v-row justify="center">
                <h3 v-if="validationStatus === 'done' && valexaIsValid === true">{{ $t('validation.pass') }}</h3>
                <h3 v-else-if="validationStatus === 'done' && valexaIsValid === false">{{ $t('validation.fail') }}</h3>
                <h3 v-else>{{$t('validation.article') }}</h3>
            </v-row>
            <v-divider dark></v-divider>
            <v-row v-if="validationStatus === 'start'" justify="center">
                <LoadingProgress/>
            </v-row>
            <v-row v-if="validationStatus === 'done'" justify="center">
                <ArticleStatusTable/>
            </v-row>
            <v-row v-if="validationStatus === 'done'" justify="center">
                <v-btn color="success" text @click="setValidationAccepted()">{{ $t('validation.accept') }}</v-btn>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
    import ValidationProgress from "./ValidationProgress";
    import ArticleStatusTable from "./ArticleStatusTable";
    import { mapMutations, mapGetters, mapState } from 'vuex'
    import LoadingProgress from "./LoadingProgress";
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "loading-page",
        components: {
            LoadingProgress,
            ValidationProgress,
            ArticleStatusTable
        },
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
            if (this.validationStatus !== 'done') {
                this.setStateLoading(true)

                ipcRenderer.on("VALID_INFO", (event, args) => {
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

                ipcRenderer.on("VALID_NAME", (event, args) => {
                    this.setValidationCurrentName(args.validationName)
                })

                ipcRenderer.on("VALID_PASS", (event, args) => {
                    this.incrementValidationCurrentNumber()
                    this.incrementValidationPass()
                    this.addValidationDescription("pass")
                })

                ipcRenderer.on("VALID_FAIL", (event, args) => {
                    this.incrementValidationCurrentNumber()
                    this.incrementValidationFail()
                    this.addValidationDescription("fail")
                })

                loadBalancer.start(ipcRenderer, 'validate')
            }
        },
    }
</script>

<style scoped>

</style>
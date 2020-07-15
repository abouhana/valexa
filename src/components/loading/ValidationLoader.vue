<template>
    <v-card
            shaped
            light
            :loading="stateLoading.validation"
    >
        <v-card-title>{{ validationText.title }}</v-card-title>
        <v-card-text class="black--text">
            <v-row justify="center">
                    <h2 v-if="loadingStatus.validation === 'start'">{{ validationText.started }}</h2>
                    <h2 v-else-if="loadingStatus.validation === 'done'">{{ validationText.done }}</h2>
                    <h2 v-else>{{ validationText.loading }}</h2>
            </v-row>
            <v-row justify="center">
                <h3 v-if="loadingStatus.validation === 'done' && valexaIsValid === true">{{ validationText.pass }}</h3>
                <h3 v-else-if="loadingStatus.validation === 'done' && valexaIsValid === false">{{ validationText.fail }}</h3>
                <h3 v-else-if="loadingStatus.validation === 'start'">{{ validationText.article }}</h3>
            </v-row>
            <v-divider dark></v-divider>
            <v-row v-if="loadingStatus.validation === 'start'" justify="center">
                <LoadingProgress/>
            </v-row>
            <v-row v-if="loadingStatus.validation === 'done'" justify="center">
                <ArticleStatusTable :table-text="validationText.tableText"/>
            </v-row>
            <v-row v-if="loadingStatus.validation === 'done'" justify="center">
                <v-btn color="success" text @click="setValidationAccepted()">{{ validationText.accept }}</v-btn>
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
                'setLoadingStatus',
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
                'loadingStatus',
                'stateLoading'
            ]),

            ...mapGetters([
                'getValidationProgress'
            ])
        },
        props: {
            validationText: Object
        },

        mounted() {
            if (this.loadingStatus.validation !== 'done') {
                this.setStateLoading({name: 'validation', status: true})

                ipcRenderer.on("VALID_INFO", (event, args) => {
                    this.setValidationTotalNumber(args.numberOfValidation)
                    if (args.status === "start") {
                        this.setLoadingStatus({name: 'validation', status: "start"})
                    } else if (args.status === "done") {
                        this.setStateLoading({name: 'validation', status: false})
                        this.setLoadingStatus({name: 'validation', status: "done"})
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
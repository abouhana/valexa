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
                <h3 v-if="loadingStatus.validation === 'done' && validation.valexaIsValid === true">{{ validationText.pass }}</h3>
                <h3 v-else-if="loadingStatus.validation === 'done' && validation.valexaIsValid === false">{{ validationText.fail }}</h3>
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
        name: "ValidationLoader",
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
                'setValidationCurrent',
                'setValexaIsValidTrue',
                'setLoadingStatus',
                'addValidationDescription',
                'setValidationAccepted',
                'setStateLoading'
            ])
        },
        computed: {
            ...mapState([
                'validation',
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
                var profileStartTimeMultiple, profileEndTimeMultiple, profileStartTimeSingle, profileEndTimeSingle
                this.setStateLoading({name: 'validation', status: true})

                ipcRenderer.on("VALID_INFO", (event, args) => {
                    switch(args.type) {

                        case 'VALID_INFO':
                            this.setValidationTotalNumber(args.data.number_of_validation)
                                if (args.data.status === "start") {
                                    this.setLoadingStatus({name: 'validation', status: "start"})
                                } else if (args.data.status === "done") {
                                    this.setStateLoading({name: 'validation', status: false})
                                    this.setLoadingStatus({name: 'validation', status: "done"})
                                    if (this.validation.validationPass === this.validation.validationTotalNumber) {
                                        this.setValexaIsValidTrue()
                                    }
                                }
                            break

                        case 'VALID_NAME':
                            this.setValidationCurrent({name: args.data.validation_name, testedProfile: args.data.tested_profile})
                            break

                        case 'VALID_PASS':
                            this.incrementValidationCurrentNumber()
                            this.incrementValidationPass()
                            this.addValidationDescription("pass")
                            break

                        case 'VALID_FAIL':
                            this.incrementValidationCurrentNumber()
                            this.incrementValidationFail()
                            this.addValidationDescription("fail")
                            break
                    }
                })

                loadBalancer.start(ipcRenderer, 'validate')
            }
        },
    }
</script>

<style scoped>

</style>
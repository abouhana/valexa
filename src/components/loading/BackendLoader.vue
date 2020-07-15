<template>
    <v-card
            shaped
            light
            :loading="stateLoading.backend"
    >
        <v-card-title>{{ backendText.title }}</v-card-title>
        <v-card-text class="black--text">
            <v-row justify="center">
                <h2 v-if="stateLoading.backend === true">{{ backendText.loading }}</h2>
                <h2 v-else>{{ backendText.done }}</h2>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
    import {mapGetters, mapMutations, mapState} from "vuex";
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "BackendLoader",
        methods: {
            ...mapMutations([
                'setStateLoading',
                'setLoadingStatus',
                'addProfileParam',
                'addModelParam'
            ])
        },
        computed: {
            ...mapState([
                'stateLoading',
                'loadingStatus'
            ])
        },
        props: {
            backendText: Object
        },
        mounted() {
            if (this.loadingStatus.backend !== 'done') {
                this.setStateLoading({name: 'backend', status: true})

                ipcRenderer.on("PARAMS_LIST", (event, args) => {
                    switch (args.type) {
                        case 'PARAMS_LIST':
                            args.data.forEach(param => this.addProfileParam(param))
                            break;

                        case 'MODEL_LIST':
                            console.log(args.data)
                            for (const [name, model] of Object.entries(args.data)) {
                                console.log(name)
                                this.addModelParam({
                                    name: name,
                                    formula: model.formula,
                                    weight: model.weight,
                                    minPoint: model.min_points
                                })
                            }
                            break;

                        case 'DONE':
                            this.setStateLoading({name: 'backend', status: 'done'})
                            this.setStateLoading({name: 'backend', status: false})
                            break;
                    }

                })

                loadBalancer.start(ipcRenderer, 'get_params')
            }
        }
    }
</script>

<style scoped>

</style>
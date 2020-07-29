<template>
    <v-row>
        <v-col>
            <v-card class="secondary" shaped elevation="2">
                <v-card-title>{{ languageText.title }}</v-card-title>
                <v-subheader>Number of thread</v-subheader>

                <v-card-text>
                    <v-slider
                        :value="profiler.maxWorkers"
                        :steps="maxCpu"
                        :max="maxCpu"
                        ticks
                        thumb-label="always"
                        @change="updateMaxWorkers"
                    ></v-slider>
                    <v-btn
                        @click="startThread"
                    >
                        Initialize
                    </v-btn>
                    <v-data-table
                            :items="items"
                            :headers="headers"
                    />
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import {mapGetters, mapMutations, mapState} from 'vuex'
    const cpus = require('os').cpus().length
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "ThreadManager",
        props: {
            languageText: Object
        },
        computed: {
            ...mapGetters([
                'getNumberOfProfiler'
            ]),
            ...mapState([
                'profiler'
            ]),
            items: function () {
                var itemArray = []
                for (var [key, value] of Object.entries(this.profiler.worker)) {
                    itemArray.push({
                        name: key,
                        status: value.status,
                        workingOn: value.workingOn
                    })
                }
                console.log(itemArray)
                return itemArray
            },
            maxCpu: () => (cpus)
        },
        methods: {
            ...mapMutations([
                'setProfilerWorkerState',
                'addProfilerWorker',
                'setMaxWorkers'
            ]),
            startThread: function() {
                if (this.getNumberOfProfiler === 0 && !this.profiler.running) {
                    for (var j=0; j<this.profiler.maxWorkers; j++ ) {
                        loadBalancer.start(ipcRenderer, 'profiler' + j)
                        this.addProfilerWorker({name: 'profiler' + j})
                    }
                }
            },
            updateMaxWorkers: function(ref) {
                this.setMaxWorkers({max: ref})
            }
        },
        data: () => ({
            threadCpu: 1,
            headers: [
                {
                    text: 'Worker name',
                    value: 'name'
                },
                {
                    text: 'Status',
                    value: 'status'
                },
                {
                    text: 'Job',
                    value: 'workingOn'
                }
            ]
        })
    }
</script>

<style scoped>

</style>
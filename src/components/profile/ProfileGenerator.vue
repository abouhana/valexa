<template>
    <div>
        <v-btn
            @click="profilerManager"
        >
            Gen
        </v-btn>
        <v-btn
            @click="closeAll"
        >
            Close
        </v-btn>
        <v-btn
            @click="logProfileToTest"
        >
            Print
        </v-btn>
    </div>
</template>

<script>
    import { mapGetters, mapState, mapMutations } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "ProfileGenerator",
        computed: {
            ...mapGetters([
                'getProfileToTest',
                'getNumberOfProfiler',
                'getFreeWorker'
            ]),
            ...mapState([
                'profiler'
            ])
        },
        methods: {
            ...mapMutations([
                'setProfilerState',
                'setProfilerWorkerState',
                'makeProfileList',
                'addProfilerWorker',
                'increaseProfilerListLocation',
                'setProfileToTest',
                'setProfileStatusDone',
                'destroyWorker'
            ]),
            logProfileToTest: function () {
                this.setProfileToTest()
                console.log(this.getProfileToTest)
            },
            profilerManager: function () {

                console.log('Number of profiler: ' + this.getNumberOfProfiler)
                console.log('Number of profile to test: ' + this.getProfileToTest.length)

                for (var i=0; i<this.getNumberOfProfiler;i++) {
                    if (i<this.getProfileToTest.length) {
                        this.generateProfile('profiler' + i, i)
                    }
                }
                this.setProfilerState({parameter: 'running', status: true})
            },
            closeAll: function () {
                for (var i=0; i<this.getNumberOfProfiler; i++){
                    loadBalancer.stop(ipcRenderer, 'profiler' + i);
                    this.destroyWorker({name: 'profiler' + i})
                }
            },
            generateProfile: function (worker, profileNumber) {
                loadBalancer.sendData(ipcRenderer, worker, {
                    data: this.getProfileToTest[profileNumber]
                });
                this.setProfilerWorkerState({worker: worker, status: 'running', workingOn: profileNumber})
                this.increaseProfilerListLocation()
            },

        },
        mounted() {
            ipcRenderer.on('INIT_STATUS', (events, args) => {
                this.setProfilerWorkerState({worker: args, status: 'idle', workinOn: null})
            })

            ipcRenderer.on('PROFILE', (events, args) => {
                if (args.data === "STOP") {
                    this.setProfileStatusDone({id: this.profiler.worker[args.profiler].workingOn})
                    this.setProfilerWorkerState({worker: args.profiler, status: 'idle', workingOn: ''})
                    if (this.profiler.listLocation<this.getProfileToTest.length) {
                        this.generateProfile(args.profiler, this.profiler.listLocation)
                    } else {
                        if (this.getFreeWorker.length === 0) {
                            this.setProfilerState({parameter: 'running', status: false})
                            loadBalancer.sendData(ipcRenderer, args.profiler, {
                                data: 'EXIT'
                            });
                            this.destroyWorker({name: args.profiler})
                        }
                    }
                } else if (args.data !== 'START') {
                    this.makeProfileList(args.data)
                }

            })
        },
        beforeDestroy() {
            if (!this.profiler.running) {
                loadBalancer.stopAll()
            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div>
        <v-btn
            @click="generateProfile"
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
    const cpus = require('os').cpus().length;

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
                'setProfileToTest'
            ]),
            logProfileToTest: function () {
                this.setProfileToTest()
                console.log(this.getProfileToTest)
            },
            profilerManager: function () {
                console.log(this.getNumberOfProfiler)
                for (var i=0; i<this.getNumberOfProfiler;i++) {
                    if (i<this.getProfileToTest.length) {
                        console.log(this.profiler.listLocation)
                        loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                            data: this.getProfileToTest[i]
                        });
                        this.setProfilerWorkerState({worker: 'profiler' + i, status: 'running'})
                        console.log('Starting worker profiler' + i)
                        this.increaseProfilerListLocation()
                    }
                }
                this.setProfilerState({parameter: 'running', status: true})
            },
            closeAll: function () {
                for (var i=0; i<cpus; i++){
                    loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                        data: 'EXIT'
                    });
                }
            },
            generateProfile: function (worker, profileNumber) {
                loadBalancer.sendData(ipcRenderer, worker, {
                    data: this.getProfileToTest[profileNumber]
                });
                this.setProfilerWorkerState({worker: worker, status: 'running'})
                this.increaseProfilerListLocation()
            }
        },
        mounted() {
            //if (this.getNumberOfProfiler === 0 && !this.profiler.running) {
            //    for (var i=0; i<4; i++ ) {
            //        loadBalancer.start(ipcRenderer, 'profiler' + i)
            //        console.log('profiler' + i + " loaded")
            //        this.addProfilerWorker({name: 'profiler' + i})
            //    }
            //}

            ipcRenderer.on('PROFILE', (events, args) => {
                if (args.data === "STOP") {
                    this.setProfilerWorkerState({worker: args.profiler, status: 'idle'})
                    console.log('Stopping worker ' + args.profiler)
                    if (this.profiler.listLocation<this.getProfileToTest.length) {
                        this.increaseProfilerListLocation()
                        console.log(this.profiler.listLocation)
                        loadBalancer.sendData(ipcRenderer, args.profiler, {
                            data: this.getProfileToTest[this.profiler.listLocation]
                        });
                        this.setProfilerWorkerState({worker: args.profiler, status: 'running'})
                        console.log('Starting worker ' + args.profiler)
                    } else {
                        console.log('Done')
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
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
            CloseAll
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
                'addProfilerWorker'
            ]),
            generateProfile: function () {
                console.log(this.getNumberOfProfiler)
                for (var i=0; i<this.getNumberOfProfiler;i++) {
                    if (i<this.getProfileToTest.length) {
                        this.setProfilerState({parameter: 'listLocation', status: i})
                        loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                            data: this.getProfileToTest[i]
                        });
                        this.setProfilerWorkerState({worker: 'profiler' + i, status: 'running'})
                        console.log('Starting worker profiler' + i)
                    }
                }
                this.setProfilerState({parameter: 'running', status: true})
            },
            closeAll: function () {
                for (var i=0; i<1; i++){
                    loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                        data: 'EXIT'
                    });
                }
            }
        },
        mounted() {
            if (this.getNumberOfProfiler > 0 && !this.profiler.running) {
                for (var i=0; i<cpus; i++ ) {
                    loadBalancer.start(ipcRenderer, 'profiler' + i)
                    console.log('profiler' + i + " loaded")
                    this.addProfilerWorker({name: 'profiler' + i})
                }
            }

            ipcRenderer.on('PROFILE', (events, args) => {
                console.log(args)
                if (args.data === "STOP") {
                    this.setProfilerWorkerState({worker: args.profiler, status: 'idle'})
                    console.log('Stopping worker ' + args.profiler)
                } else {
                    this.makeProfileList(args.data)
                }

            })
        },
        watch: {
            getFreeWorker: function () {
                if (this.getFreeWorker>0) {
                    const worker = this.getFreeWorker[0]
                    this.setProfilerState({parameter: 'listLocation', status: this.profiler.listLocation++})
                    loadBalancer.sendData(ipcRenderer, worker, {
                        data: this.getProfileToTest[this.profiler.listLocation]
                    });
                    this.setProfilerWorkerState({worker: worker, status: 'running'})
                    console.log('Starting worker ' + worker)
                }
            }
        }
    }
</script>

<style scoped>

</style>
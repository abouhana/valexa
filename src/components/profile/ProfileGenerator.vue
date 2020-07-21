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
                'getNumberOfProfiler'
            ]),
            ...mapState([
                'profiler'
            ])
        },
        methods: {
            ...mapMutations([
               'setProfilerState'
            ]),
            generateProfile: function () {
                for (var i=0; i<4; i++){
                    loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                        data: this.getProfileToTest[i]
                    });
                }
            },
            closeAll: function () {
                for (var i=0; i<4; i++){
                    loadBalancer.sendData(ipcRenderer, 'profiler' + i, {
                        data: 'EXIT'
                    });
                }
            }
        },
        mounted() {
            if (this.getNumberOfProfiler < cpus && !this.profiler.running) {
                for (var i=0; i<cpus; i++ ) {
                    loadBalancer.start(ipcRenderer, 'profiler' + i, {dataExtra: 'aaa'})
                    console.log('profiler' + i + " loaded")
                    //this.addProfilerWorker({name: 'profiler' + i})
                }
                this.setProfilerState({status: true})
            }

            ipcRenderer.on('PROFILE', (events, args) => {
                if (args.data === "START") {
                    this.setStateLoading({name: 'profiles', status: true})
                } else if (args.data === "STOP") {
                    this.setStateLoading({name: 'profiles', status: true})
                    this.finishListOfProfile()
                } else {
                    //this.makeProfileList(args.data)
                }

            })
        }
    }
</script>

<style scoped>

</style>
<template>
    <v-row>
        <v-col>
            <v-card class="secondary" shaped elevation="2">
                <v-card-title>{{ languageText.title }}</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col>
                            {{ languageText.description }}
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            {{ languageText.numberOfProfile }} {{getListLocation}}/{{ estimatedNumberOfProfile }}
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            {{ languageText.estimatedTime }} {{ estimatedTime }}
                        </v-col>
                    </v-row>
                    <div>
                        <v-btn
                                @click="startThread"
                        >
                            Gen
                        </v-btn>
                        <v-btn
                        >
                            Close
                        </v-btn>
                        <v-btn
                        >
                            Print
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import { mapState,mapGetters,mapMutations } from 'vuex'
    import ThreadManager from "./ThreadManager";
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')


    export default {
        name: "ProfileHeader",
        components: {
            ThreadManager
        },
        props: {
            languageText: Object
        },
        computed: {
            ...mapGetters([
                'getListOfCompound',
                'getSettingForCompound',
                'compoundHasCalibration',
                'getTableConfig',
                'getAverageTimePerProfile',
                'getProfileToTest',
                'getListLocation',
                'getNumberOfWorker'
            ]),
            ...mapState([
               'profiler'
            ]),
            estimatedNumberOfProfile: function () {
                var numberOfProfile = 0
                this.getListOfCompound.forEach((compound) => {
                    var validationNumber = 1
                    var calibrationNumber = 1
                    var numberOfModel = this.getSettingForCompound({compound: compound, setting: 'model_to_test'}).length
                    if (this.getSettingForCompound({compound: compound, setting: 'rolling_data'})) {
                        var maxSize = this.getTableConfig({compound: compound, dataType: 'validation'}).numberOfLevel
                        var minSize = this.getSettingForCompound({compound: compound, setting: 'rolling_limit'})
                        if (typeof minsize === 'object') {
                            minSize = minSize[0]
                        }
                        validationNumber = [...Array(maxSize - minSize + 1).keys()].map(x => x + 1).reduce((a, b) => a + b)
                        if (this.compoundHasCalibration({compound: compound})) {
                            maxSize = this.getTableConfig({compound: compound, dataType: 'calibration'}).numberOfLevel
                            minSize = this.getSettingForCompound({compound: compound, setting: 'rolling_limit'})

                            if (typeof minsize === 'object') {
                                minSize = minSize[0]
                            }
                            calibrationNumber = [...Array(maxSize - minSize + 1).keys()].map(x => x + 1).reduce((a, b) => a + b)
                        }
                    }
                    numberOfProfile += validationNumber*calibrationNumber*numberOfModel
                })
                return numberOfProfile
            },
            estimatedTime: function () {
                return this.estimatedNumberOfProfile*this.getAverageTimePerProfile/1000
            },
            initStatus: function () {
                return this.profiler.status === 'ready' && this.profiler.running;
            }
        },
        methods: {
            ...mapMutations([
                'addProfilerWorker',
                'setProfilerState',
                'setProfileToTest',
                'setProfilerWorkerState',
                'increaseProfilerListLocation'
            ]),
            startThread: function() {
                this.setProfilerState({parameter: 'running', status: true})
                if (this.getNumberOfWorker === 0) {
                    for (var j=0; j<this.profiler.maxWorkers; j++ ) {
                        this.addProfilerWorker({name: 'profiler' + j})
                        loadBalancer.start(ipcRenderer, 'profiler' + j)
                    }
                }
            },
            startProfileGeneration: function () {

                for (var i=0; i<this.getNumberOfWorker;i++) {
                    if (i<this.getProfileToTest.length) {
                        this.generateProfile('profiler' + i, i)
                    }
                }
                this.setProfilerState({parameter: 'running', status: true})
            },
            generateProfile: function (worker, profileNumber) {
                loadBalancer.sendData(ipcRenderer, worker, {
                    data: this.getProfileToTest[profileNumber]
                });
                this.setProfilerWorkerState({worker: worker, status: 'running', workingOn: profileNumber})
                this.increaseProfilerListLocation()
            },
        },
        watch: {
            initStatus(newValue, oldValue) {
                if (newValue && newValue !== oldValue) {
                    this.setProfileToTest()
                    this.startProfileGeneration()
                }
            }
        }
    }
</script>

<style scoped>

</style>
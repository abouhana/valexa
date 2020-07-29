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
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import { mapState,mapGetters,mapMutations } from 'vuex'
    import ProfileGenerator from "./ProfileGenerator";
    import ThreadManager from "./ThreadManager";


    export default {
        name: "SettingHeader",
        components: {ThreadManager, ProfileGenerator},
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
                'getListLocation'
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
            }
        }
    }
</script>

<style scoped>

</style>
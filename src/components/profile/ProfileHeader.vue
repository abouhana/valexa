<template>
    <v-row>
        <v-col>
        <v-card class="secondary" shaped elevation="2">
            <v-card-title>{{ languageText.title }}</v-card-title>
            <v-card-text>
                <v-row>
                    <v-col>
                        {{ languageText.description }} {{ estimatedNumberOfProfile }}
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        {{ languageText.numberOfProfile }} {{ estimatedNumberOfProfile }}
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import { mapState,mapGetters,mapMutations } from 'vuex'


    export default {
        name: "SettingHeader",
        props: {
            languageText: Object
        },
        computed: {
            ...mapGetters([
                'getListOfCompound',
                'getSettingForCompound',
                'checkIfCompoundHasCalibration',
                'getTableConfig'
            ]),
            estimatedNumberOfProfile: function () {
                var numberOfProfile = 0
                this.getListOfCompound.forEach((compound) => {
                    var numberOfModel = this.getSettingForCompound({compound: compound, setting: 'model_to_test'}).length
                    var maxSize = this.getTableConfig({compound: compound, dataType: 'validation'}).numberOfLevel
                    var minSize = this.getSettingForCompound({compound: compound, setting: 'rolling_limit'})
                    console.log(JSON.stringify(minSize))
                    if (typeof minsize === 'object') {
                        minSize = minSize[0]
                    }
                    console.log(maxSize)
                    console.log(minSize)
                    var validationNumber = [...Array(maxSize-minSize+1).keys()].map(x => x+1).reduce((a,b) => a+b)
                    var calibrationNumber = 1
                    if (this.checkIfCompoundHasCalibration({compound: compound})) {
                        maxSize = this.getTableConfig({compound: compound, dataType: 'calibration'}).numberOfLevel
                        minSize = this.getSettingForCompound({compound: compound, setting: 'rolling_limit'})

                        if (typeof minsize === 'object') {
                            minSize = minSize[0]
                        }
                        calibrationNumber = [...Array(maxSize-minSize+1).keys()].map(x => x+1).reduce((a,b) => a+b)
                    }
                    numberOfProfile += validationNumber*calibrationNumber*numberOfModel
                })
                return numberOfProfile
            }
        }
    }
</script>

<style scoped>

</style>
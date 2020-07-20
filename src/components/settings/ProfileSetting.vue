<template>
    <v-col>
        <v-card
                light
                shaped
                elevation="2"
        >
            <v-card-title>Profile Setting</v-card-title>
            <v-card-text>
                <v-text-field
                        outlined
                        label="Tolerance Limit"
                        rounded
                        dense
                        v-model.number="toleranceLimit"
                        type="number"
                        persistent-hint
                        hint="Tolerance limits in percent. This correspond to a two-tailed Student's T value."
                />
                <v-text-field
                        outlined
                        label="Acceptance Limit"
                        rounded
                        dense
                        v-model.number="acceptanceLimit"
                        type="numeric"
                        persistent-hint
                        hint="Acceptance limits in percentage. This is the maximum accepted variation from the expected value."
                />
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
    import { mapGetters, mapMutations, mapState } from 'vuex'

    export default {
        name: "ProfileSetting",
        props: {
            languageText: Object,
            settingsName: String
        },
        computed: {
            ...mapGetters([
                'getSettingsValue'
            ]),
            toleranceLimit: {
                get () {
                    return this.getSettingsValue({
                        name:this.settingsName,
                        setting: 'tolerance_limit'
                    })
                },
                set (value) {
                    this.setSettingsValue({
                        name:this.settingsName,
                        setting: 'tolerance_limit',
                        value: value
                    })
                }
            },
            acceptanceLimit: {
                get () {
                    return this.getSettingsValue({
                        name:this.settingsName,
                        setting: 'acceptance_limit'
                    })
                },
                set (value) {
                    this.setSettingsValue({
                        name:this.settingsName,
                        setting: 'acceptance_limit',
                        value: value
                    })
                }
            }
        },
        methods: {
            ...mapMutations([
                'setSettingsValue'
            ])
        }
    }
</script>

<style scoped>

</style>
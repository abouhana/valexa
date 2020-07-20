<template>
    <v-col>
        <v-card
                light
                shaped
                elevation="2"
        >
            <v-card-title>General Setting</v-card-title>
            <v-card-text>
                <v-autocomplete
                        outlined
                        label="Compound Name"
                        placeholder="Compound Name"
                        rounded
                        dense
                        v-model="compoundName"
                        type="text"
                        persistent-hint
                        hint="Enter the name of the compounds this settings apply to, leave blank to apply to every compounds not overwritten by other settings."
                        multiple
                        :items="formattedListOfItems"
                        menu-props="light"
                        item-text="text"
                        item-disabled="disabled"
                >
                    <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index <= 1" small>
                            <span>{{ item.text }}</span>
                        </v-chip>
                        <span
                            v-if="index === 2"
                            class="grey--text caption"
                        >
                            (+{{ getListOfCompound.length - 2 }} {{languageText.moreCompounds}})
                        </span>
                    </template>
                </v-autocomplete>
                <v-text-field
                        outlined
                        label="Unit"
                        placeholder="Unit"
                        rounded
                        dense
                        v-model="quantityUnits"
                        type="text"
                        persistent-hint
                        hint="Unit (%, mg/kg, ppm, etc.) for the validation report."
                />
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
    import { mapGetters, mapMutations, mapState } from 'vuex'

    export default {
        name: "GeneralSetting",
        props: {
            languageText: Object,
            settingsName: String
        },
        computed: {
            ...mapGetters([
                'getListOfCompound',
                'getSettingsValue'
            ]),
            quantityUnits: {
                get () {
                    return this.getSettingsValue({
                        name:this.settingsName,
                        setting: 'quantity_units'
                    })
                },
                set (value) {
                    this.setSettingsValue({
                        name:this.settingsName,
                        setting: 'quantity_units',
                        value: value
                    })
                }
            },
            compoundName: {
                get () {
                    return this.getSettingsValue({
                        name: this.settingsName,
                        setting: 'appliesTo'
                    })
                },
                set (value) {
                    let currentArray = this.getSettingsValue({
                        name:this.settingsName,
                        setting: 'appliesTo'
                    })
                    if (currentArray.length > value.length) {
                        let difference = currentArray.filter(x => !value.includes(x))[0]
                        console.log(difference)
                        this.moveCompoundToSetting({compound: difference, setting: 'default'})
                    } else {
                        let difference = value.filter(x => !currentArray.includes(x))[0]
                        console.log(difference)
                        this.moveCompoundToSetting({compound: difference, setting: this.settingsName})
                    }

                }
            },
            formattedListOfItems: function () {
                var compoundList = []
                var settingsName = this.settingsName
                this.getListOfCompound.forEach(function (item) {
                    compoundList.push({
                        text: item,
                        disabled: settingsName === 'default'
                    })
                })
                return compoundList
            }
        },
        methods: {
            ...mapMutations([
                'setSettingsValue',
                'moveCompoundToSetting'
            ])
        },
        data: () => ({
        })
    }
</script>

<style scoped>

</style>
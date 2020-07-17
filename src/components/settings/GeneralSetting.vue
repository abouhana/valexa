<template>
    <v-col>
        <v-card
                light
                shaped
                elevation="2"
        >
            <v-card-title>General Setting</v-card-title>
            <v-card-text>
                <v-text-field
                        outlined
                        label="Compound Name"
                        placeholder="Compound Name"
                        rounded
                        dense
                        v-model="compoundName"
                        type="text"
                        persistent-hint
                        hint="Enter the name of the compounds this settings apply to, leave blank to apply to every compounds not overwritten by other settings."
                />
                <v-text-field
                        outlined
                        label="Unit"
                        placeholder="Unit"
                        rounded
                        dense
                        v-model="quantityUnit"
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
            generalText: Object
        },
        computed: {
            ...mapState([
                'profileParams'
            ])
        },
        data: () => ({
            compoundName: '',
            quantityUnit: ''
        })
    }
</script>

<style scoped>

</style>
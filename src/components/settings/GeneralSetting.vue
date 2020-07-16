<template>
    <v-col>
        <v-card
                light
                shaped
                rounded
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
                />
                <v-text-field
                        outlined
                        label="Unit"
                        placeholder="Unit"
                        rounded
                        dense
                        v-model="quantityUnit"
                        type="text"
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
<template>
    <v-col>
        <v-card
                light
                shaped
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
                />
                <v-text-field
                        outlined
                        label="Acceptance Limit"
                        rounded
                        dense
                        v-model.number="acceptanceLimit"
                        type="numeric"
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
            profileText: Object
        },
        computed: {
            ...mapState([
                'profileParams'
            ])
        },
        data: () => ({
            toleranceLimit: '',
            acceptanceLimit: '',
        })
    }
</script>

<style scoped>

</style>
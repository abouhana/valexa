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
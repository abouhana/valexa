<template>
    <v-row justify="center">
        {{ validationCurrentName }}
    </v-row>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: "LoadingProgress",
        computed: {
            ...mapState([
                'validationCurrentName'
            ]),
        }
    }
</script>

<style scoped>

</style>
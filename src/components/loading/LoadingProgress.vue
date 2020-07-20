<template>
    <v-row justify="center">
        {{ validation.validationCurrent.name }}
    </v-row>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: "LoadingProgress",
        computed: {
            ...mapState([
                'validation'
            ]),
        }
    }
</script>

<style scoped>

</style>
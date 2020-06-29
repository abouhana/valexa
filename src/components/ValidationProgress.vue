<template>
    <loading-progress
        :progress="progress"
        :indeterminate="indeterminate"
        :counter-clockwise="counterClockwise"
        :hide-background="hideBackground"
        shape="line"
        size="40"
        width="200"
        height="40"
    />
</template>

<script>
    import 'vue-progress-path/dist/vue-progress-path.css'

    export default {
        name: "ValidationProgress",

        props: {
            progress: {
                "default": 0
            }
        },

        data () {
            return {
                indeterminate: false,
                counterClockwise: false,
                hideBackground: true
            }
        }
    }


</script>

<style scoped>

</style>
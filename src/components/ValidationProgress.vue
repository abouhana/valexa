<template>
    <loading-progress
        :progress="progress"
        :indeterminate="indeterminate"
        :counter-clockwise="counterClockwise"
        :hide-background="hideBackground"
        shape="line"
        size="200"
        width="200"
        height="6"
    />
</template>

<script>
    import 'vue-progress-path/dist/vue-progress-path.css'

    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "ValidationProgress",

        data () {
            return {
                indeterminate: false,
                progress: "progress",
                counterClockwise: false,
                hideBackground: false
            }
        },
        mounted() {
            ipcRenderer.on("VALID_PROGRESS",  (event, args) => {
                this.progress = parseInt(args.data)/100
            })

            loadBalancer.start( ipcRenderer ,'validate')
        },
    }


</script>

<style scoped>

</style>
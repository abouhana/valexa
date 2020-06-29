<template>
    <div>Test mainpage</div>
</template>

<script>
    import { mapMutations, mapGetters, mapState } from 'vuex'
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {


        name: "MainPage",

        mounted() {
            loadBalancer.start( ipcRenderer ,'test')
        }
    }
</script>

<style scoped>

</style>
<template>
    <h1>
        {{ messageShown }}
        Validating: {{ validationName }}
    </h1>
</template>

<script>
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "LoadingPage",
        data () {
            return {
                messageShown: "Please wait",
                currentValidation: "",
                numberOfValidation: "",
                numberOfFail: "",
                numberOfPass: "",
                validationName: ""
            }
        },
        mounted() {
            ipcRenderer.on("VALID_INFO",  (event, args) => {
                this.numberOfValidation = args.numberOfValidation
                this.numberOfFail = args.numberOfFail
                this.numberOfPass = args.numberOfPass
                if (args.status == "start") {
                    this.messageShown = "I am currently validating myself."
                } else if (args.status == "done") {
                    if (this.numberOfPass == this.numberOfValidation) {
                        this.messageShown = "All is good, I am valid :)"
                    } else {
                        this.messageShown = "There seem to be a problem with me :("
                    }
                }
            })

            ipcRenderer.on("VALID_NAME",  (event, args) => {
                this.validationName = args.validationName
            })
        },
    }
</script>

<style scoped>

</style>
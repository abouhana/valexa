<template>
    <div id="loading">
        <v-row
                justify="center"
                align="center"
        >
        <h2>{{ messageShown }}</h2>
        </v-row>
        <v-row
                justify="center"
                align="stretch"
        >
            <div class="view">
                <ValidationProgress v-bind:progress="progress"></ValidationProgress>
            </div>
        </v-row>
        <v-row
                justify="center"
                align="start"
        >
            Validating against: {{ validationName }} <br>
            Pass: {{numberOfPass}} out of {{ numberOfValidation }} <br>
            Fail: {{numberOfFail}} out of {{ numberOfValidation }}
        </v-row>
    </div>
</template>

<script>
    import ValidationProgress from "../components/ValidationProgress";
    const electron = require('electron')
    const ipcRenderer = electron.ipcRenderer
    const loadBalancer = require('electron-load-balancer')

    export default {
        name: "LoadingPage",
        components: {ValidationProgress},
        data () {
            return {
                messageShown: "Please wait",
                currentValidation: "",
                numberOfValidation: 0,
                numberOfFail: 0,
                numberOfPass: 0,
                validationName: "",
                progress: 0
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

            ipcRenderer.on("VALID_PASS",  (event, args) => {
                this.progress = parseInt(args.numberOfPass)/this.numberOfValidation
                this.numberOfPass = args.numberOfPass
            })

            ipcRenderer.on("VALID_PASS",  (event, args) => {
                this.numberOfFail = args.numberOfFail
            })

            loadBalancer.start( ipcRenderer ,'validate')
        },
    }
</script>

<style scoped>

</style>
<i18n>
    {
        "en": {
            "title": "Initialization",
            "validation": {
                "title": "Verification",
                "loading": "Please wait while I load.",
                "started": "I am validating myself",
                "done": "All done!",
                "pass": "Everything looks good :)",
                "fail": "There seems to be a problems :(",
                "article": "I am currently testing myself against:",
                "accept": "Accept the verification to continue",
                "tableText": {
                    "article": "Article",
                    "status": "Status",
                    "runningTime": "Running Time",
                    "averageTime": "Per Profile Time",
                    "average": "Average"
                }
            },
            "backend" : {
                "title": "Valexa Engine",
                "loading": "Firing up my engine",
                "done": "Ready to roll"
            }
        },
        "fr": {
            "title": "Initialisation",
            "validation": {
                "title": "Vérification",
                "loading": "Veuillez patienter pendant que je me charge",
                "started": "Je suis en train de me valider",
                "done": "Fini!",
                "pass": "Tout semble bien :)",
                "fail": "On dirait qu'il y a un problème :(",
                "article": "Je m'évalue présentement selon:",
                "accept": "Accepter la vérification pour continuer",
                "tableText": {
                    "article": "Article",
                    "status": "Statut",
                    "runningTime": "Temps d'exécution",
                    "averageTime": "Temps par profile",
                    "average": "Moyenne"
                }
            },
            "backend" : {
                "title": "Moteur Valexa",
                "loading": "Chauffage des moteurs",
                "done": "Prêt à partir"
            }
        }
    }
</i18n>

<template>
    <div>
        <h1>{{ $t('title') }}</h1>
        <v-row>
            <v-col>
                <BackendLoader :backend-text="$t('backend')"/>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <ValidationLoader :validation-text="$t('validation')"/>
            </v-col>
        </v-row>

    </div>
</template>

<script>
    import ValidationLoader from "../components/loading/ValidationLoader";
    import BackendLoader from "../components/loading/BackendLoader";

    export default {
        name: "LoadingView",
        components: {BackendLoader, ValidationLoader },
    }
</script>

<style scoped>

</style>
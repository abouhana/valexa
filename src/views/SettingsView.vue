<i18n>
    {
        "en": {
            "table": {
                "lblSeries": "Series",
                "lblLevel": "Level",
                "lblRep": "Replicate",
                "lblSupp": "Additional Row",
                "btnAdd": "Add Row",
                "btnReset": "Reset Data",
                "btnResize": "Resize Table",
                "validation": "Validation",
                "calibration": "Calibration",
                "data": {
                    "series": "Series",
                    "level": "Level",
                    "x": "X",
                    "y": "Replicate ",
                    "validation": "Validation Data",
                    "calibration": "Calibration Data"
                }
            }
        },
        "fr": {
            "table": {
                "lblSeries": "Série",
                "lblLevel": "Niveau",
                "lblRep": "Réplicat",
                "lblSupp": "Rangée Supplémentaire",
                "btnAdd": "Ajouter une rangé",
                "btnReset": "Effacer les données",
                "btnResize": "Redimensionner le tableau",
                "validation": "Validation",
                "calibration": "Calibration",
                "data": {
                    "series": "Série",
                    "level": "Niveau",
                    "x": "X",
                    "y": "Repétition ",
                    "validation": "Données de Validation",
                    "calibration": "Données de Calibration"
                }
            }
        }
    }
</i18n>

<template>
    <SettingsManager/>
</template>

<script>
    import SettingsManager from "../components/settings/SettingsManager";
    export default {
        name: "SettingsView",
        components: {SettingsManager}
    }
</script>

<style scoped>

</style>
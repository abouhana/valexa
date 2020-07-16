<i18n>
    {
        "en": {
            "series": "Series",
            "level": "Level",
            "x": "X",
            "y": "Replicate ",
            "validation": "Validation Data",
            "calibration": "Calibration Data"
        },
        "fr": {
            "series": "Série",
            "level": "Niveau",
            "x": "X",
            "y": "Repétition ",
            "validation": "Données de Validation",
            "calibration": "Données de Calibration"
        }
    }
</i18n>

<template>
    <v-row justify="center">
        <v-col>
            <TableConfig
                data-type="validation"
            />
        </v-col>
        <v-col>
            <TableConfig
                data-type="calibration"
            />
        </v-col>
    </v-row>
</template>

<script>
    import TableConfig from "../components/data/TableConfig";
    import DataTable from "../components/data/DataTable";

    export default {
        name: 'data-view',
        components: {
            DataTable,
            TableConfig
        }
    }
</script>

<style scoped>
</style>
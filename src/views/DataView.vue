
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
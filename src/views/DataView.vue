
<template>

    <v-row justify="center">
        <v-col>
            <v-row justify="center">
                <v-col>
                    <v-text-field
                            outlined
                            label="Series"
                            placeholder="Number of Series"
                            rounded
                            dense
                            >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            label="Levels"
                            placeholder="Number of Levels"
                            rounded
                            dense
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            label="Repetitions"
                            placeholder="Number of Repetitions"
                            rounded
                            dense
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row justify="center">
                <DataTable
                        :number-of-series="3"
                        :number-of-level="5"
                        :number-of-rep="2"
                        data-type="validation"
                />
            </v-row>
        </v-col>
        <v-col>
            <DataTable
                    :number-of-series="3"
                    :number-of-level="5"
                    :number-of-rep="2"
                    data-type="calibration"
            />
        </v-col>
    </v-row>
</template>

<script>
    import DataTable from "../components/data/DataTable";

    export default {
        name: 'data-view',
        components: {
            DataTable
        }
    }
</script>

<style scoped>
</style>
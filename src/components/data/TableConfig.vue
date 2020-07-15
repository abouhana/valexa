<template>
    <v-card
            shaped
            light
    >
        <v-card-title>{{ dataType }}</v-card-title>
        <v-card-text>
            <v-row justify="center">
                <v-col>
                    <v-text-field
                            outlined
                            label="Series"
                            placeholder="Number of Series"
                            rounded
                            dense
                            @input="updateDataTable(numberOfSeries)"
                            v-model.number="numberOfSeries"
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
                            @input="updateDataTable(numberOfLevel)"
                            v-model.number="numberOfLevel"
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
                            @input="updateDataTable(numberOfRep)"
                            v-model.number="numberOfRep"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row justify="center">
                <DataTable
                        :number-of-series="numberOfSeries"
                        :number-of-level="numberOfLevel"
                        :number-of-rep="numberOfRep"
                        :data-type="dataType"
                        :key="componentKey"
                />
            </v-row>
            <v-row justify="center">
                <v-btn
                        text
                >Add Row</v-btn>
                <v-btn
                    text
                >Reset</v-btn>
                <v-btn
                    text
                >Resize</v-btn>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
    import DataTable from "./DataTable";

    export default {
        name: "TableConfig",
        components: {
            DataTable
        },
        props: {
            dataType: String
        },
        data: () => ({
            componentKey: 0,
            numberOfRep: 2,
            numberOfLevel: 3,
            numberOfSeries: 3
        }),
        methods: {
            updateDataTable: function (value) {
                if (value !== "") {
                    this.componentKey = !this.componentKey
                }
            }
        }
    }
</script>

<style scoped>

</style>
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
                            v-model.number="numberOfRep"
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            label="Additional row"
                            placeholder="Additional row"
                            rounded
                            dense
                            v-model.number="numberOfSupp"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <DataTable
                    :number-of-series="numberOfSeries"
                    :number-of-level="numberOfLevel"
                    :number-of-rep="numberOfRepetition"
                    :number-of-supp="numberOfSupp"
                    :data-type="dataType"
                    :key="componentKey"
            />
            <v-row justify="center">
                <v-btn
                        text
                        @click="addRow()"
                >Add Row</v-btn>
                <v-btn
                    text
                    @click="resetTable()"
                >Reset</v-btn>
                <v-btn
                    text
                    @click="updateDataTable()"
                >Resize</v-btn>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
    import DataTable from "./DataTable";
    import { mapMutations, mapGetters, mapState } from 'vuex'

    export default {
        name: "TableConfig",
        components: {
            DataTable
        },
        props: {
            dataType: String
        },
        computed: {
            ...mapState([
                'tableData'
            ])
        },
        data: () => ({
            componentKey: 0,
            numberOfRep: 2,
            numberOfLevel: 3,
            numberOfSeries: 3,
            numberOfRepetition: 2,
            numberOfSupp: 0
        }),
        methods: {
            ...mapMutations([
                'emptyEnteredData'
            ]),
            updateDataTable: function () {
                this.numberOfRepetition = this.numberOfRep
                this.componentKey = !this.componentKey
            },
            addRow: function () {
                this.numberOfSupp++
                this.componentKey = !this.componentKey
            },
            resetTable: function () {
                this.emptyEnteredData(this.dataType)
                this.componentKey = !this.componentKey
            }
        }
    }
</script>

<style scoped>

</style>
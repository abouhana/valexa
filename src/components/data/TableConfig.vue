<template>
    <v-card
            shaped
            light
    >
        <v-card-title>{{ tableText[dataType] }}</v-card-title>
        <v-card-text>
            <v-row justify="center">
                <v-col>
                    <v-text-field
                            outlined
                            :label="tableText.lblSeries"
                            rounded
                            dense
                            v-model.number="numberOfSeries"
                            type="number"
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            :label="tableText.lblLevel"
                            rounded
                            dense
                            v-model.number="numberOfLevel"
                            type="number"
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            :label="tableText.lblRep"
                            rounded
                            dense
                            v-model.number="numberOfRep"
                            type="number"
                    >
                    </v-text-field>
                </v-col>
                <v-col>
                    <v-text-field
                            outlined
                            :label="tableText.lblSupp"
                            rounded
                            dense
                            v-model.number="numberOfSupp"
                            type="number"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <DataTable
                    :number-of-series="getTableConfig(dataType).numberOfSeries"
                    :number-of-level="getTableConfig(dataType).numberOfLevel"
                    :number-of-rep="getTableConfig(dataType).numberOfRep"
                    :number-of-supp="getTableConfig(dataType).numberOfSupp"
                    :data-type="dataType"
                    :key="componentKey"
                    :data-text="tableText.data"
            />
            <v-row justify="center">
                <v-btn
                        text
                        @click="addRow()"
                >{{ tableText.btnAdd }}</v-btn>
                <v-btn
                    text
                    @click="resetTable()"
                >{{ tableText.btnReset }}</v-btn>
                <v-btn
                    text
                    @click="updateDataTable()"
                >{{ tableText.btnResize }}</v-btn>
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
            dataType: String,
            tableText: Object,
        },
        computed: {
            ...mapGetters([
                'getTableConfig'
            ]),
        },
        data: () => ({
            componentKey: 0,
            numberOfLevel: 0,
            numberOfSeries: 0,
            numberOfRep: 0,
            numberOfSupp: 0

        }),
        mounted: function () {
            this.numberOfLevel = this.getTableConfig(this.dataType).numberOfLevel
            this.numberOfSeries = this.getTableConfig(this.dataType).numberOfSeries
            this.numberOfRep = this.getTableConfig(this.dataType).numberOfRep
            this.numberOfSupp = this.getTableConfig(this.dataType).numberOfSupp
        },
        methods: {
            ...mapMutations([
                'emptyEnteredData',
                'setTableConfig'
            ]),
            updateDataTable: function () {
                var data = {
                    dataType: this.dataType,
                    data: {
                        numberOfLevel: this.numberOfLevel,
                        numberOfSeries: this.numberOfSeries,
                        numberOfRep: this.numberOfRep,
                        numberOfSupp: this.numberOfSupp
                    }
                }
                this.setTableConfig(data)
                this.componentKey = !this.componentKey
            },
            addRow: function () {
                this.numberOfSupp++
                this.updateDataTable()
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
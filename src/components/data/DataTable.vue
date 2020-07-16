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
    <v-row class="black--text" justify="center" :key="componentKey">
        <vue-excel-editor no-header-edit v-model="tableData" @update="updateData" no-paging>
            <vue-excel-column field="series" :label="$t('series')" type="number"/>
            <vue-excel-column field="level" :label="$t('level')" type="number"/>
            <vue-excel-column field="x" :label="$t('x')" type="number"/>
            <vue-excel-column
                    v-for="rep in this.numberOfRep"
                    :field="'y' + rep"
                    :label="$t('y') + rep"
                    :key="rep"
                    type="number"
            />
        </vue-excel-editor>
    </v-row>
</template>

<script>
    import { mapMutations, mapGetters, mapState } from 'vuex'

    export default {
        name: "DataTable",
        props: {
            numberOfSeries: [Number, String],
            numberOfLevel: [Number, String],
            numberOfRep: [Number, String],
            numberOfSupp: [Number],
            dataType: String,
        },
        data: () => ({
            tableData: [],
            componentKey: 0
        }),
        mounted: function () {
            if (this.getEnteredData(this.dataType).length === 0) {
                this.createTable()
            } else {
                this.modifyTable()
            }
        },
        computed: {
            ...mapGetters([
                'getEnteredData'
            ]),
        },
        methods: {
            ...mapMutations([
                'setEnteredData'
            ]),
            createTable: function () {
                for (var series = 1; series <= this.numberOfSeries; series++) {
                    for (var level = 1; level <= this.numberOfLevel; level++) {
                        this.tableData.push({
                            series: series,
                            level: level
                        })
                    }
                }
                for (var supp = 0; supp < this.numberOfSupp; supp++) {
                    this.tableData.push({})
                }
            },
            modifyTable: function () {
                const currentTableData = this.getEnteredData(this.dataType)
                var tempTableData = []
                for (var series = 1; series <= this.numberOfSeries; series++) {
                    for (var level = 1; level <= this.numberOfLevel; level++) {
                        if (typeof currentTableData.find( row => row.series === series && row.level === level) !== 'undefined') {
                            tempTableData.push(currentTableData.find( row => row.series === series && row.level === level))
                            //TODO: remove saved Y
                        } else {
                            tempTableData.push({
                                series: series,
                                level: level
                            })
                        }
                    }
                }
                for (var supp = 0; supp < this.numberOfSupp; supp++) {
                    tempTableData.push({})
                }
                this.tableData = tempTableData
            },
            updateData: function () {
                this.setEnteredData({ dataType: this.dataType, tableData: this.tableData})
            }
        },
    }
</script>

<style scoped>

</style>
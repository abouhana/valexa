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
    <div class="black--text">
        <vue-excel-editor no-header-edit v-model="tableData" @update="updateData">
            <vue-excel-column field="series" :label="$t('series')" />
            <vue-excel-column field="level" :label="$t('level')" />
            <vue-excel-column field="x" :label="$t('x')" />
            <vue-excel-column
                    v-for="rep in this.numberOfRep"
                    :field="'y' + rep"
                    :label="$t('y') + rep"
                    :key="rep"
            />
        </vue-excel-editor>
    </div>
</template>

<script>
    import { mapMutations, mapGetters, mapState } from 'vuex'

    export default {
        name: "DataTable",
        props: {
            numberOfSeries: Number,
            numberOfLevel: Number,
            numberOfRep: Number,
            dataType: String,
        },
        data: () => ({
            tableData: []
        }),
        mounted: function () {
            if (this.getEnteredData(this.dataType).length === 0) {
                this.createTable()
            } else {
                this.tableData = this.getEnteredData(this.dataType)
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
                for (var serie = 1; serie <= this.numberOfSeries; serie++) {
                    for (var level = 1; level <= this.numberOfLevel; level++) {
                        this.tableData.push({
                            series: serie,
                            level: level
                        })
                    }
                }
            },
            updateData: function () {
                this.setEnteredData({ dataType: this.dataType, tableData: this.tableData})
            }
        },
    }
</script>

<style scoped>

</style>
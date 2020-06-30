<template>
    <v-container>
        <v-row>
            <v-col>
                <div class="chart-container" style="position: relative;">
                    <line-chart :chart-data="accuracyProfileData" :options="options"></line-chart>
                </div>
            </v-col>
            <v-col>
                <div class="chart-container" style="position: relative;">
                    <line-chart :chart-data="linearityProfileData" :options="options"></line-chart>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import LineChart from './ProfileChartJs'
    import { mapGetters } from "vuex"

    export default {
        components: {
            LineChart
        },

        methods: {
            absoluteModeSwitch: function () {
                if (this.absoluteAcceptance===true) {
                    return "abs"
                } else {
                    return "rel"
                }
            },
        },

        props: {
            xAxeString: String,
            yAxeString: String,
            profileId: Number,
            absoluteAcceptance: Boolean
        },

        computed: {

            ...mapGetters([
               'getProfile'
            ]),

            profileData: function () {
                return this.getProfile(this.profileId)
            },

            accuracyProfileData: function () {
                var dataObject = {}
                var labels = []
                var acc = this.absoluteModeSwitch()
                const graphList = {}
                const errorBars = {}

                for (const [key, value] of Object.entries(this.profileData)) {
                    if (key === "graph") {
                        const graphVar = [
                            "recovery",
                            "acceptance_limits_" + acc + "_high",
                            "acceptance_limits_" + acc + "_low",
                            "error",
                            "tolerance_" + acc + "_high",
                            "tolerance_" + acc + "_low"
                        ]
                        graphVar.forEach((value) => {
                            graphList[value] = []
                        })
                        for (const graph_value of Object.values(value)) {
                            for (const item of Object.keys(graphList)) {
                            graphList[item].push(
                                    {
                                        "x": graph_value["introduced_concentration"],
                                        "y": graph_value[item]
                                    }
                                )
                            }
                        }
                    } else if (key === "scatter") {
                        var scatterPoint = value
                    }
                }

                for (var i=0; i < graphList["recovery"].length; i++ ) {
                    labels.push("Level " + (i+1))
                }
                dataObject["labels"] = labels

                dataObject["labels"].forEach(function (label, index) {
                    errorBars[label] = {
                     plus: graphList["error"][index]["y"],
                     minus: -graphList["error"][index]["y"]
                 }
                })

                dataObject["datasets"] = [
                    {
                        label: "Acceptance Limit",
                        fill: false,
                        borderColor: "orange",
                        lineTension: 0,
                        borderDash: [10,10],
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["acceptance_limits_" + acc + "_high"]
                    },
                    {
                        label: "none",
                        fill: false,
                        borderColor: "orange",
                        lineTension: 0,
                        borderDash: [10,10],
                        pointRadius: 0,
                        data: graphList["acceptance_limits_" + acc + "_low"]
                    },
                    {
                        label: "Tolerance Limit",
                        fill: false,
                        borderColor: "green",
                        lineTension: 0,
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["tolerance_" + acc + "_high"]
                    },
                    {
                        label: "none",
                        fill: false,
                        borderColor: "green",
                        lineTension: 0,
                        pointRadius: 0,
                        data: graphList["tolerance_" + acc + "_low"]
                    },
                    {
                        label: "Recovery",
                        fill: false,
                        borderColor: "blue",
                        borderDash: [5, 5, 10, 10],
                        lineTension: 0,
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["recovery"],
                        errorBars: errorBars
                    },
                    {
                        label: "Scatter",
                        fill: false,
                        borderColor: "black",
                        showLine: false,
                        data: scatterPoint,
                        type: "scatter"
                    }
                ]

                return dataObject
            },

            linearityProfileData: function () {
                const dataObject = {}
                const scatterPoints = []
                const scatterPointRaw = []
                var hasCorrection = false
                var labels = []
                let colorArray = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
                    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
                    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
                    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
                    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
                    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

                if (this.profileData["model_info"]["correction_factor"] > 0) {
                    hasCorrection = true
                }

                this.profileData["model_info"]["list_of_series_validation"].forEach(value => {
                    scatterPoints[value] = []
                    labels.push("Serie " + value)
                })

                this.profileData["validation_data"].forEach( (dataPoint) => {
                    scatterPoints[dataPoint["Serie"]].push({
                        x: dataPoint["x"],
                        y: dataPoint["x_calc"]
                    })
                })

                if (hasCorrection) {
                    for (const dataPoint in Object.values(this.profileData["validation_data"])){
                        scatterPoints[dataPoint["Serie"]].push({
                            x: dataPoint["x"],
                            y: dataPoint["x_raw"]
                        })
                    }
                }

                dataObject["labels"] = labels
                dataObject["datasets"] = []

                scatterPoints.forEach(function (dataPoint, label){
                    dataObject["datasets"].push(
                        {
                            label: "Serie " + label,
                            fill: false,
                            borderColor: colorArray[label],
                            showLine: false,
                            data: dataPoint,
                            type: "scatter"
                        }
                    )
                })

                return dataObject

            },

            options: function () {
                const layout = {padding: 50}
                const responsive = true
                const legend = {
                    labels: {
                        filter: function (item) {
                            return item.text == null || !item.text.includes('none');
                        },
                        usePointStyle: true
                    }
                }

                var scales = {
                    xAxes: [{
                        type: 'linear',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: this.xAxeString
                        },
                    }],
                        yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: this.yAxeString
                        }
                    }]
                }

                return {layout: layout, responsive: responsive, legend: legend, scales: scales}

            }
        },

        data () {
            return {

            }
        }
    }


</script>

<style scoped>
</style>
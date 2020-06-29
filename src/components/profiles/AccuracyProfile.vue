<template>
    <v-container>
        <div class="chart-container" style="position: relative;">
            <line-chart :chart-data="dataCollection" :options="options"></line-chart>
        </div>
    </v-container>
</template>

<script>
    import LineChart from './ProfileChartJs'

    export default {
        components: {
            LineChart
        },

        methods: {
            returnJson: function () {
                return JSON.parse('{\n' +
                    '  "graph": [\n' +
                    '    {\n' +
                    '      "introduced_concentration": 1.9000000000000001,\n' +
                    '      "recovery": 93.64406672852874,\n' +
                    '      "tol_limit_low": 26.505410756319858,\n' +
                    '      "tol_limit_high": 160.78272270073762,\n' +
                    '      "acc_limit_low": 80,\n' +
                    '      "acc_limit_high": 120,\n' +
                    '      "error": 84.33259846316163\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "introduced_concentration": 4.7,\n' +
                    '      "recovery": 100.33099312858967,\n' +
                    '      "tol_limit_low": 83.16354160287855,\n' +
                    '      "tol_limit_high": 117.49844465430076,\n' +
                    '      "acc_limit_low": 80,\n' +
                    '      "acc_limit_high": 120,\n' +
                    '      "error": 19.091713992959775\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "introduced_concentration": 9.5,\n' +
                    '      "recovery": 101.92752577281237,\n' +
                    '      "tol_limit_low": 83.97126625133296,\n' +
                    '      "tol_limit_high": 119.88378529429178,\n' +
                    '      "acc_limit_low": 80,\n' +
                    '      "acc_limit_high": 120,\n' +
                    '      "error": 21.73721563100102\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "introduced_concentration": 28.5,\n' +
                    '      "recovery": 99.74489293496109,\n' +
                    '      "tol_limit_low": 94.45816126918002,\n' +
                    '      "tol_limit_high": 105.03162460074216,\n' +
                    '      "acc_limit_low": 80,\n' +
                    '      "acc_limit_high": 120,\n' +
                    '      "error": 6.489057951739105\n' +
                    '    }\n' +
                    '  ],\n' +
                    '  "scatter": [\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 57.757506220170335\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 58.404039867218565\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 157.4552531339154\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 85.48904351446153\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 98.5129675644238\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 1.9,\n' +
                    '      "y": 104.2455900709829\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 92.96846389772921\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 89.17442641125835\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 110.37111020939865\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 102.91926109927451\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 105.39004794469055\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 4.7,\n' +
                    '      "y": 101.16264920918651\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 91.51457245611569\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 92.89647242204236\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 106.137233007347\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 111.95816171247905\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 112.04568157703814\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 9.5,\n' +
                    '      "y": 97.01303346185196\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 101.87481319993755\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 103.4000368849118\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 99.66900771249853\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 95.83096468835534\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 100.339832979874\n' +
                    '    },\n' +
                    '    {\n' +
                    '      "x": 28.5,\n' +
                    '      "y": 97.35470214418935\n' +
                    '    }\n' +
                    '  ]\n' +
                    '}')
    }
        },

        props: {
          xAxeString: String,
          yAxeString: String,

        },


        computed: {

            dataCollection: function () {
                var fullData = this.returnJson()
                var dataObject = {}
                var labels = []

                for (const [key, value] of Object.entries(fullData)) {
                    if (key === "graph") {
                        var graphList = {
                            "recovery": [],
                            "acc_limit_high": [],
                            "acc_limit_low": [],
                            "error": [],
                            "tol_limit_high": [],
                            "tol_limit_low": []
                        }
                        for (const [graph_key, graph_value] of Object.entries(value)) {
                            for (const item of [
                                "recovery",
                                "acc_limit_high",
                                "acc_limit_low",
                                "error",
                                "tol_limit_high",
                                "tol_limit_low"
                            ]) {
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


                dataObject["datasets"] = [
                    {
                        label: "Acceptance Limit",
                        fill: false,
                        borderColor: "orange",
                        lineTension: 0,
                        borderDash: [10,10],
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["acc_limit_high"]
                    },
                    {
                        label: "none",
                        fill: false,
                        borderColor: "orange",
                        lineTension: 0,
                        borderDash: [10,10],
                        pointRadius: 0,
                        data: graphList["acc_limit_low"]
                    },
                    {
                        label: "Tolerance Limit",
                        fill: false,
                        borderColor: "green",
                        lineTension: 0,
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["tol_limit_high"]
                    },
                    {
                        label: "none",
                        fill: false,
                        borderColor: "green",
                        lineTension: 0,
                        pointRadius: 0,
                        data: graphList["tol_limit_low"]
                    },
                    {
                        label: "Recovery",
                        fill: false,
                        borderColor: "blue",
                        borderDash: [5, 5, 10, 10],
                        lineTension: 0,
                        pointRadius: 0,
                        pointStyle: 'line',
                        data: graphList["recovery"]
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

            options2: function () {
                const layout = {padding: 50}
                const responsive = true
                const legend = {
                        filter: function (item) {
                            return item.text == null || !item.text.includes('none');
                        },
                        usePointStyle: true
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
                options: {
                    layout: {
                        padding: 50
                    },
                    responsive: true,
                    scales: {
                         xAxes: [{
                               type: 'linear',
                               display: true,
                               scaleLabel: {
                                    display: true,
                                    labelString: 'Concentration'
                               },
                          }],
                         yAxes: [{
                             display: true,
                             scaleLabel: {
                                 display: true,
                                 labelString: 'Deviation'
                             }
                         }]
                    },
                    legend: {
                        labels: {
                            filter: function (item) {
                                return item.text == null || !item.text.includes('none');
                            },
                            usePointStyle: true
                        }
                    }
                }
            }
        }
    }


</script>

<style scoped>
</style>
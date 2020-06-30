<script>
    import { Line, mixins, generateChart } from 'vue-chartjs'
    import chartjsPluginErrorBars from 'chartjs-plugin-error-bars'

    export default {
        extends: Line,
        props: ['chartData', 'options'],
        mixins: [mixins.reactiveProp],
        mounted () {
            this.addPlugin(chartjsPluginErrorBars),
            this.renderChart(this.chartData, this.options)
        }
    }
</script>

<style scoped>

</style>
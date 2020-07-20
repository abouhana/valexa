<template>
    <v-data-table
            class="no-scroll"
            :items="validation.validationDescription"
            :headers="headers"
            dense
            hide-default-footer
    >
        <template v-slot:item.status="{ item }">
            <v-icon v-if="item.status === 'pass'" color="green">mdi-check</v-icon>
            <v-icon v-else color="red">mdi-alert</v-icon>
        </template>
        <template v-slot:body.append="{body}">
            <tr>
                <td v-for="(header,i) in headers" :key="i">
                    <div v-if="header.value === 'runningTime'">
                        <strong>{{ tableText.average }}</strong>
                    </div>
                    <div v-if="header.value === 'averageTime'">
                        {{ Math.round(getAverageTimePerProfile) }} ms
                    </div>
                    <div v-else>
                    </div>
                </td>
            </tr>
        </template>
    </v-data-table>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'

    export default {
        name: "ArticleStatusTable",
        computed: {
            ...mapState([
                'validation'
            ]),
            ...mapGetters([
               'getAverageTimePerProfile'
            ]),
            headers: function () {
                return [
                    { text: this.tableText.article, value: 'name' },
                    { text: this.tableText.status, value: 'status' },
                    { text: this.tableText.runningTime, value: 'runningTime' },
                    { text: this.tableText.averageTime, value: 'averageTime' },
                ]
            }
        },
        props: {
            tableText: Object
        }
    }
</script>

<style scoped>

</style>
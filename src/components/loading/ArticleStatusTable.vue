<template>
    <v-data-table
            class="no-scroll"
            :items="validationDescription"
            :headers="headers"
            dense
            hide-default-footer
    >
        <template v-slot:item.status="{ item }">
            <v-icon v-if="item.status === 'pass'" color="green">mdi-check</v-icon>
            <v-icon v-else color="red">mdi-alert</v-icon>
        </template>
    </v-data-table>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: "ArticleStatusTable",
        computed: {
            ...mapState([
                'validationDescription'
            ]),
            headers: function () {
                return [
                    { text: this.tableText.article, value: 'name' },
                    { text: this.tableText.status, value: 'status' },
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
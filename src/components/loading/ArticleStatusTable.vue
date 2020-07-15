<template>
    <v-simple-table class="no-scroll">
        <template v-slot:default>
            <thead>
                <tr>
                    <th>Article</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tr v-for="validation in validationDescription">
                <td>{{ validation.name }}</td>
                <td>
                    <v-icon v-if="validation.status === 'pass'" color="green">mdi-check</v-icon>
                    <v-icon v-else color="red">mdi-alert</v-icon>
                </td>
            </tr>
        </template>
    </v-simple-table>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        name: "ArticleStatusTable",
        computed: {
            ...mapState([
                'validationDescription'
            ])

        }
    }
</script>

<style scoped>

</style>
<template>
    <v-expansion-panel light flat>
        <v-expansion-panel-header>
            {{compoundName}}
        </v-expansion-panel-header>
        <v-expansion-panel-content justify="center">
            <v-card shaped elevation="2">
                <v-card-text>
                    <v-row>
                        <v-col>
                            <ProfileTable/>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
    export default {
        name: "ProfileCard"
    }
</script>

<style scoped>

</style>
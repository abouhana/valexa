<template>
    <v-expansion-panel light flat>
        <v-expansion-panel-header>
            {{compoundName}} - {{getProfilesTable({compoundName: compoundName}).length}} profiles
        </v-expansion-panel-header>
        <v-expansion-panel-content justify="center">
            <v-card shaped elevation="2">
                <v-card-text>
                    <v-row>
                        <v-col>
                            <ProfileTable :compound-name="compoundName"/>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
    import ProfileTable from "./ProfileTable";
    import {mapGetters} from 'vuex'

    export default {
        name: "ProfileCard",
        components:{
          ProfileTable
        },
        props: {
          compoundName: String
        },
        computed: {
          ...mapGetters([
              'getProfilesTable'
          ])
        }
    }
</script>

<style scoped>

</style>
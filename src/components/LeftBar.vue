<template>
    <v-list
            dense
            shaped
    >
        <v-list-item-group>
            <v-list-item
                    v-for="(item, i) in items"
                    :key="i"
                    :to="item.to"
            >
                <v-list-item-action>
                    <v-icon v-text="item.icon"></v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title v-text="item.text"></v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list-item-group>
    </v-list>
</template>

<script>
    export default {
        name: "LeftBar",

        data () {
            return {
                items: {
                    main: {
                        icon: 'mdi-home',
                        text: 'Home',
                        to: '/'
                    },
                    settings: {
                        icon: 'mdi-tune',
                        text: 'Settings',
                        to: 'settings'
                    },
                    data: {
                        icon: 'mdi-table',
                        text: 'Data',
                        to: 'data'
                    },
                    profile: {
                        icon: 'mdi-chart-line',
                        text: 'Profiles',
                        to: 'profiles'
                    },
                }
            }
    }
    }
</script>

<style scoped>

</style>
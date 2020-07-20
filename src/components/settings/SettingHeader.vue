<template>
    <v-row>
        <v-col>
        <v-card class="secondary" shaped elevation="2">
            <v-card-title>{{ languageText.title }}</v-card-title>
            <v-card-text>
                <v-row>
                    <v-col>
                        {{ languageText.description }}
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: "SettingHeader",
        props: {
            languageText: Object
        }
    }
</script>

<style scoped>

</style>
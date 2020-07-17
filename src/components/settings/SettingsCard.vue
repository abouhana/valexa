<template>
    <v-card class="secondary" shaped elevation="2">
        <v-card-title>Settings</v-card-title>
        <v-card-text>
            <v-row>
                <GeneralSetting/>
                <ProfileSetting/>
            </v-row>
            <v-row>
                <AdvancedSetting/>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
    import GeneralSetting from "./GeneralSetting";
    import ProfileSetting from "./ProfileSetting";
    import AdvancedSetting from "./AdvancedSetting";

    export default {
        name: "SettingsCard",
        components: {
            AdvancedSetting,
            GeneralSetting,
            ProfileSetting
        }
    }
</script>

<style scoped>

</style>
<template>
    <div>
        <v-row>
            <GeneralSetting/>
            <ProfileSetting/>
        </v-row>
        <v-row>
            <AdvancedSetting/>
        </v-row>
    </div>
</template>

<script>
    import GeneralSetting from "./GeneralSetting";
    import ProfileSetting from "./ProfileSetting";
    import AdvancedSetting from "./AdvancedSetting";
    export default {
        name: "SettingsManager",
        components: {
            AdvancedSetting,
            GeneralSetting,
            ProfileSetting
        }
    }
</script>

<style scoped>

</style>
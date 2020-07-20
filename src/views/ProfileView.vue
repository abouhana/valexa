<i18n>
    {
        "en": {
            "header": {
                "title": "Settings",
                "description": "Description",
                "numberOfProfile": "Estimated number of profile to be generated"
            },
            "card": {
                "settings" : "Settings",
                "enterSettings": "Add settings",
                "default": "Default",
                "lblSetting": "Settings",
                "hintSetting": "Enter a name for these settings",
                "btnContinue": "Continue",
                "btnEdit": "Edit Name",
                "btnSave": "Save",
                "errNameEmpty": "The name must not be empty",
                "errNameExist": "This compound already exist",
                "btnDelete": "Delete these setting",
                "advanced": {
                    "correction": {
                        "selectTrue": "Yes",
                        "selectFalse": "No"
                     },
                    "modelization": {
                        "moreModel": " others models",
                        "selectTrue": "Yes",
                        "selectFalse": "No"
                    }
                },
                "general": {
                    "moreCompounds": " others compounds"
                },
                "profile": {
                }
            }
        },
        "fr": {
            "header": {
                "title": "Settings",
                "description": "Description",
                "numberOfProfile": "Estimated number of profile to be generated"
            },
            "card": {
                "settings" : "Compound",
                "entersettings": "Add a compound to continue",
                "default": "Par défaut",
                "lblsettings": "Compound",
                "hintsettings": "Enter the name of the compound or target for these data",
                "btnContinue": "Continue",
                "btnEdit": "Edit Name",
                "btnSave": "Save",
                "errNameEmpty": "The name must not be empty",
                "errNameExist": "This compound already exist",
                "btnDelete": "Delete this compound",
                "advanced": {
                    "correction": {
                        "selectTrue": "Yes",
                        "selectFalse": "No"
                     },
                    "modelization": {
                        "moreModel": " autres modèles",
                        "selectTrue": "Oui",
                        "selectFalse": "Non"
                    }
                },
                "general": {
                    "moreCompounds": " autres composés"
                },
                "profile": {
                }
            }
        }
    }
</i18n>

<template>
    <div>
        <SettingHeader :language-text="$t('header')"/>
        <ProfileTable/>
    </div>
</template>

<script>
    import ProfileTable from "../components/profile/ProfileTable";
    import SettingHeader from "../components/profile/ProfileHeader";

    export default {

        name: "profile-view",
        components: {
            SettingHeader,
            ProfileTable,
        },
    }
</script>

<style scoped>

</style>
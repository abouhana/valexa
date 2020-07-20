<template>
    <v-expansion-panel light flat>
        <v-expansion-panel-header>
            <template v-slot:default="{ open }">
                <v-row class="text-h5">
                    <span v-if="settingsName==='default'">{{languageText.default}}</span>
                    <span v-else-if="!!settingsName">{{settingsName}}</span>
                    <span v-else>{{ languageText.enterSettings }}</span>
                </v-row>
            </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content justify="center">
            <v-card shaped elevation="2">
                <v-card-text>
                    <v-row>
                        <v-col>
                            <v-text-field
                                    outlined
                                    rounded
                                    :label="languageText.lblSettings"
                                    :placeholder="languageText.settings"
                                    dense
                                    :hint="languageText.hintSettings"
                                    v-model="settingsName"
                                    :disabled="!editingMode"
                                    :rules="[settingsNameRules]"
                                    :error-messages="errorMessages"
                                    @keypress.enter="updateName()"
                            />
                            <span v-if="settingsName !== 'default'">>
                                <v-btn
                                        text
                                        @click="updateName()"
                                >
                                    {{ continueBtnText }}
                                </v-btn>
                                <v-btn
                                        v-if="nameEntered"
                                        text
                                        @click="destroy()"
                                >
                                    {{ languageText.btnDelete }}
                                </v-btn>
                            </span>
                        </v-col>
                    </v-row>
                        <v-row v-if="nameEntered">
                            <GeneralSetting :settings-name="savedSettingsName" :language-text="languageText.general"/>
                            <ProfileSetting :settings-name="savedSettingsName" :language-text="languageText.profile"/>
                        </v-row>
                        <v-row>
                            <AdvancedSetting :settings-name="savedSettingsName" :language-text="languageText.advanced"/>
                        </v-row>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
    import GeneralSetting from "./GeneralSetting";
    import ProfileSetting from "./ProfileSetting";
    import AdvancedSetting from "./AdvancedSetting";
    import {mapGetters, mapMutations} from "vuex";

    export default {
        name: "SettingsCard",
        components: {
            AdvancedSetting,
            GeneralSetting,
            ProfileSetting
        },
        props: {
            languageText: Object,
            loadDataFrom: {
                type: String,
                default: ''
            }
        },
        computed: {
            ...mapGetters([
                'getListOfSettings'
            ]),
            continueBtnText: function () {
                if (this.settingsNameState === 'init') {
                  return this.languageText.btnContinue
                } else if (this.settingsNameState === 'saved') {
                  return this.languageText.btnEdit
                } else {
                  return this.languageText.btnSave
                }
            }
        },
        methods: {
            ...mapMutations([
                'initSettings',
                'renameSettings',
                'deleteSettings'
            ]),
            updateName: function () {
                if (this.settingsNameState === 'init') {
                    if (!this.errorMessages) {
                        this.savedSettingsName = this.settingsName
                        this.initSettings({name: this.savedSettingsName})
                        this.editingMode = false
                        this.settingsNameState = 'saved'
                        this.nameEntered = true
                    }
                } else if (this.settingsNameState === 'saved') {
                    this.editingMode = true
                    this.settingsNameState = 'edit'
                } else {
                    this.renameData({oldName: this.savedSettingsName, newName: this.settingsName})
                    this.savedSettingsdName = this.settingsName
                    this.editingMode = false
                    this.settingsNameState = 'saved'
                }
            },
            settingsNameRules: function () {
                if (!this.settingsName) {
                    this.errorMessages = this.languageText.errNameEmpty
                } else if (this.getListOfSettings.includes(this.settingsName)) {
                    this.errorMessages = this.languageText.errNameExist
                } else {
                    this.errorMessages = ''
                }

                return true
            },
            destroy: function () {
                this.deleteSettings({name: this.savedSettingsName})
            }
        },
        data: () => ({
            nameEntered: false,
            savedSettingsName: '',
            settingsNameState: 'init',
            editingMode: true,
            settingsName: null,
            errorMessages: ''
        }),
        mounted: function () {
            if (this.loadDataFrom !== '') {
                this.savedSettingsName = this.loadDataFrom
                this.settingsName = this.loadDataFrom
                this.nameEntered = true
                this.settingsNameState = 'saved'
                this.editingMode = false
            }
        }

    }
</script>

<style scoped>

</style>
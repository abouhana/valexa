<template>
    <v-expansion-panel light flat>
        <v-expansion-panel-header>
            <template v-slot:default="{ open }">
                <v-row class="text-h5">
                    <span v-if="!!compoundName">{{compoundName}}</span>
                    <span v-else>{{ languageText.enterCompound }}</span>
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
                                    :label="languageText.lblCompound"
                                    :placeholder="languageText.compound"
                                    dense
                                    persistent-hint
                                    :hint="languageText.hintCompound"
                                    v-model="compoundName"
                                    :disabled="!editingMode"
                                    :rules="[compoundNameRules]"
                                    :error-messages="errorMessages"
                                    @keypress.enter="updateName()"
                            />
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
                        </v-col>
                    </v-row>
                    <v-row v-if="nameEntered">
                        <v-col>
                            <TableConfig
                                    data-type="validation"
                                    :compound="savedCompoundName"
                                    :language-text="languageText.table"
                                    :enabled="!editingMode"
                            />
                        </v-col>
                        <v-col>
                            <TableConfig
                                    data-type="calibration"
                                    :compound="savedCompoundName"
                                    :language-text="languageText.table"
                                    :enabled="!editingMode"
                            />
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
    import TableConfig from "./TableConfig";
    import { mapMutations, mapGetters } from "vuex"

    export default {
        name: "DataCard",
        components: {TableConfig},
        props: {
            languageText: Object,
            loadDataFrom: {
                type: String,
                default: ''
            }
        },
        computed: {
            ...mapGetters([
                'getListOfCompound'
            ]),
            continueBtnText: function () {
                if (this.compoundNameState === 'init') {
                  return this.languageText.btnContinue
                } else if (this.compoundNameState === 'saved') {
                  return this.languageText.btnEdit
                } else {
                  return this.languageText.btnSave
                }
            }
        },
        methods: {
            ...mapMutations([
                'initCompoundData',
                'renameCompoundData',
                'deleteCompoundData'
            ]),
            updateName: function () {
                if (this.compoundNameState === 'init') {
                    if (!this.errorMessages) {
                        this.savedCompoundName = this.compoundName
                        this.initCompoundData({compound: this.savedCompoundName})
                        this.editingMode = false
                        this.compoundNameState = 'saved'
                        this.nameEntered = true
                    }
                } else if (this.compoundNameState === 'saved') {
                    this.editingMode = true
                    this.compoundNameState = 'edit'
                } else {
                    this.renameCompoundData({oldName: this.savedCompoundName, newName: this.compoundName})
                    this.savedCompoundName = this.compoundName
                    this.editingMode = false
                    this.compoundNameState = 'saved'
                }
            },
            compoundNameRules: function () {
                if (!this.compoundName) {
                    this.errorMessages = this.languageText.errNameEmpty
                } else if (this.getListOfCompound.includes(this.compoundName)) {
                    this.errorMessages = this.languageText.errNameExist
                } else {
                    this.errorMessages = ''
                }

                return true
            },
            destroy: function () {
                this.deleteCompoundData({name: this.savedCompoundName})
            }
        },
        data: () => ({
            nameEntered: false,
            savedCompoundName: '',
            compoundNameState: 'init',
            editingMode: true,
            compoundName: null,
            errorMessages: ''
        }),
        mounted: function () {
            if (this.loadDataFrom !== '') {
                this.savedCompoundName = this.loadDataFrom
                this.compoundName = this.loadDataFrom
                this.nameEntered = true
                this.compoundNameState = 'saved'
                this.editingMode = false
            }
        }
    }
</script>

<style scoped>

</style>
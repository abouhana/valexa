<template>
    <v-expansion-panel light flat>
        <v-expansion-panel-header>
            <template v-slot:default="{ open }">
                <v-row class="text-h5">
                    <span v-if="compoundName!==''">{{compoundName}}</span>
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
                                    dense
                                    persistent-hint
                                    :hint="languageText.hintCompound"
                                    v-model="compoundName"
                                    :disabled="!editingMode"
                            />
                            <v-btn
                                    text
                                    @click="updateName()"
                            >
                                {{ continueBtnText }}
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
    import { mapMutations } from "vuex"

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
                'renameData'
            ]),
            updateName: function () {
                if (this.compoundNameState === 'init') {
                    if (this.compoundName !== '' ) {
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
                    this.renameData({oldName: this.savedCompoundName, newName: this.compoundName})
                    this.savedCompoundName = this.compoundName
                    this.editingMode = false
                    this.compoundNameState = 'saved'
                }
            }
        },
        data: () => ({
            nameEntered: false,
            savedCompoundName: '',
            compoundNameState: 'init',
            editingMode: true,
            compoundName: ''
        }),
        mounted: function () {
            console.log(this.loadDataFrom)
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
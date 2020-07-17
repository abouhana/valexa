<template>
    <v-col>
        <v-card shaped light elevation="2">
            <v-card-text>
                <v-expansion-panels light flat accordion>
                    <v-expansion-panel>
                        <v-expansion-panel-header>Advanced Setting</v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <v-row dense>
                                <v-col dense>
                                    <v-card shaped light elevation="2">
                                        <v-card-title>Correction</v-card-title>
                                        <v-card-text>
                                            <v-select
                                                    :items="items"
                                                    outlined
                                                    rounded
                                                    dense
                                                    label="correction_allow"
                                                    persistent-hint
                                                    hint="Allow the application of a correction factor to the data."
                                                    menu-props="light, rounded"
                                            />
                                            <v-text-field
                                                    outlined
                                                    rounded
                                                    dense
                                                    label="correction_forced_value"
                                                    persistent-hint
                                                    hint="Force a specific correction factor to be applied."
                                            />
                                            <v-text-field
                                                    outlined
                                                    rounded
                                                    dense
                                                    label="correction_round_to"
                                                    persistent-hint
                                                    hint="The correction factor will be rounded to this number of significant value."
                                            />
                                            <v-text-field
                                                    outlined
                                                    rounded
                                                    dense
                                                    label="correction_threshold"
                                                    persistent-hint
                                                    hint="The average deviation or recovery threshold at which a correction factor will be generated, example: 0.8, 1.2."
                                            />
                                        </v-card-text>
                                    </v-card>
                                </v-col>
                                <v-col dense>
                                    <v-card shaped light elevation="2">
                                        <v-card-title>Modelization</v-card-title>
                                        <v-card-text>
                                        <v-select
                                                outlined
                                                rounded
                                                dense
                                                label="model_to_test"
                                        />
                                        <v-select
                                                    :items="items"
                                                    outlined
                                                    rounded
                                                    dense
                                                    label="rolling_dataw"
                                                    persistent-hint
                                                    hint="This option will try to test every data iteration possibilty and generate multiple models. This may takes a while..."
                                                    menu-props="light, rounded"
                                            />
                                        <v-text-field
                                                outlined
                                                rounded
                                                dense
                                                label="rolling_limit"
                                        />
                                        <v-text-field
                                                outlined
                                                rounded
                                                dense
                                                label="significant_figure"
                                        />
                                    </v-card-text>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-card-text>
        </v-card>
    </v-col>
</template>

<script>
    export default {
        name: "AdvancedSetting",
        data: () => ({
            items: ['Yes', 'No']
        })
    }
</script>

<style scoped lang="sass">
    .v-expansion-panel-header
        font-size: 20px
</style>
<i18n>
    {
        "en": {
            "title": "Im Alizee",
            "header": {
                "title": "Lets start playing",
                "description": "with joice please"
            }
        },
        "fr": {
            "title": "Moi c'est Alizée",
            "header": {
                "title": "Amusons nous",
                "description": "avec de la bonne humeur svp"
            }
        }
    }
</i18n>

<template>
    <div>
      <h1>{{ $t('title') }}</h1>
      <v-row>
        <v-col>
            <v-card shaped light>
              <v-card-title>Titre first CARD</v-card-title>
              <v-card-text class="black--text">
                  <v-row justify="center">
                      <h2></h2>
                  </v-row>
              </v-card-text>
          </v-card>
        </v-col>
      </v-row>



        <v-card class="secondary" shaped elevation="2">
            <v-card-text>
                <v-row>
                    <v-col>
                      Commencons par creer une liste grace a un joli composant perso fait par bibi

                      <ListModifiable></ListModifiable>  <!--appel au store dans le composant-->

                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
  import SettingHeader from "../components/profile/ProfileHeader";
  import ListModifiable from "../components/ListModifiable";

  export default {
    name: "SecondView",

    components:{
      SettingHeader,
      ListModifiable
    },

    computed:{

    },

    data:() => ({

    })
  }
</script>

<style scoped>

</style>
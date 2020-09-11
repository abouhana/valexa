<i18n>
    {
        "en": {
            "header": {
                "title": "Data Entry",
                "description": "Please enter the data for each compound"
            }
        },
        "fr": {
            "header": {
                "title": "Entrée de données",
                "description": "Entrer les données pour chacun des composés"
            }
        }
    }
</i18n>


<template>
    <div>
        <v-card class="secondary" shaped elevation="2">
            <v-card-text>
                <v-row>
                    <v-col>
                        <v-card shaped flat>
                          <compAlizee v-bind:tod="groceryList" v-bind:propE="{id: 'non', a: true}"></compAlizee>   <!--tod = props spécifique a compAlizee-->
                          <!--composant d'affichage d'une liste en lui fournissant les données-->
                        </v-card>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
  import compAlizee from "../components/compAlizee";

  export default {
    name: "FirstView",
    components:{
      compAlizee
    },
    data: () => ({
      message: 'Hello Vue !',
      groceryList: [
        { id: 'ui' }, // objet
        { id: 1, text: 'Fromage' },
        { id: 2, text: 'Tout ce que les humains sont supposés manger'}
      ] // Array d'objets
    }),
    methods: {

    }
  }
</script>

<style scoped>

</style>
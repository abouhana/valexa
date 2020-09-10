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

                          <div id="app-6">
                            <p>{{ message }}</p>
                            <input v-model="message">
                          </div>
                          <div id="app-5">
                            <p>{{ message }}</p>
                            <button v-on:click="reverseMessage">Message retourné</button>
                          </div>
                          <compAlizee
                            v-bind:tod="groceryList"
                          ></compAlizee>   <!--tod = props spécifique a compAlizee-->
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
          { id: 0, text: 'Légumes' },
        { id: 1, text: 'Fromage' },
        { id: 2, text: 'Tout ce que les humains sont supposés manger' }
      ]
    }),
    methods: {
      reverseMessage: function () {
        this.message = this.message.split('').reverse().join('')
      }
    }
  }
</script>

<style scoped>

</style>
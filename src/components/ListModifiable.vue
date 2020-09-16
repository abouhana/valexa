<template>
<v-card shaped flat>
  <ul>
    <li v-for="i in this.listeAnimaux">
      {{i.nom}} le super {{i.animal}}
      <span v-if="i.gentil" class="mdi mdi-thumb-up-outline"></span>
      <span v-else class="mdi mdi-thumb-down-outline"></span>
    </li>
  </ul>

  <br><v-btn @click="showTri()">Tri sur les animaux</v-btn>

  <v-card-text v-if="this.bTriVisible">
      <v-row>
        <v-col cols="12" sm="6" md="3">
          <v-btn @click="resetAll()">RESET</v-btn><br><br>
          <v-text-field v-model="valsTri.nom" label="Nom animal"/>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field outlined rounded dense persistent-hint label="Age minimal" type="number" v-model="valsTri.age.mini"/>
          <v-text-field outlined rounded dense persistent-hint label="Age maximal" type="number" v-model="valsTri.age.maxi"/>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-select chips label="Sélection animaux" v-model="valsTri.animal" :items="this.animaux" multiple/>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-row>
            <v-checkbox v-model="this.valsTri.ouiGentil" class="mx-2" label="gentil"></v-checkbox>
            <v-checkbox v-model="this.valsTri.nonGentil" class="mx-2" label="méchant"></v-checkbox>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
            <br><v-btn @click="trier()">Appliquer le tri</v-btn>
        </v-col>
      </v-row>
    </v-card-text>



</v-card>
</template>


<script>
  import ComposantTri from "../components/ComposantTri";
  import { mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: "ListModifiable",

    beforeMount(){
      this.resetAll()
    },

    data: () => ({
      bTriVisible: false,
      valsTri:{
        nom: String,
        age: {mini: '', maxi: ''},
        animal: [],
        ouiGentil: Boolean,
        nonGentil : Boolean
      },
      listeAnimaux: []
    }),

    computed: {
      ...mapState(['dataListAB', 'animaux',]),
      ...mapGetters(['getDataListAB'])
    },

    methods:{
      ...mapMutations(['removeDataListAB', 'addDataListAB', 'changeDataListAB', 'setDataListAB']),
      showTri: function() {
        this.resetAll()
        this.bTriVisible = !this.bTriVisible
        this.tri = !this.tri
      },
      resetAll: function() {
        this.valsTri = {
          nom: '',
          age: {mini: '', maxi: ''},
          animal: this.animaux,
          ouiGentil: true,
          nonGentil: true
        }
        this.listeAnimaux = this.dataListAB
      },
      trier: function(){
        var listResult = this.dataListAB  //init

        //nom
        if(this.valsTri.nom !== ''){
          //suppression accents: this.valsTri.nom.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
          var regex = new RegExp("(" + this.valsTri.nom + ")\\w+", "ig")
          var listeTemp = []
          listResult.forEach(animal => {
            if(animal.nom.match(regex) !== null && animal.nom.match(regex).length !== 0){
              listeTemp.push(animal)
            }
          })
          listResult = listeTemp
        }

        //age
        if(this.valsTri.age.mini !== ''){
          listResult = listResult.filter(animal => animal.age >= this.valsTri.age.mini)
        }
        if(this.valsTri.age.maxi !== ''){
          listResult = listResult.filter(animal => animal.age <= this.valsTri.age.maxi)
        }

        //gentil
        if(!this.valsTri.ouiGentil && !this.valsTri.nonGentil){
          listResult = []
        } else if(this.valsTri.ouiGentil && this.valsTri.nonGentil){

        } else if(this.valsTri.ouiGentil){
          listResult = listResult.filter(animal => animal.gentil === true)
        } else if(this.valsTri.nonGentil){
          listResult = listResult.filter(animal => animal.gentil === false)
        } // else pas de tri

        //categorie animaux
        listResult = listResult.filter(animal => this.valsTri.animal.includes(animal.animal))

        this.listeAnimaux = listResult
      },



    },





  }
</script>

<style scoped>

</style>
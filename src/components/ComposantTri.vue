<template>

</template>

<script>
  import { mapGetters, mapMutations, mapState } from 'vuex'


  export default {
    name: "ComposantTri",

    methods:{
      ...mapMutations([
          'removeDataListAB',
          'addDataListAB',
          'changeDataListAB',
          'setDataListAB'
      ]),

    },

    computed:{
      ...mapState([
          'dataListAB'
      ]),


    },

    data: () => ({

    })

  }
</script>

<style scoped>

</style>
<template>
  <div>
    <li v-for="item in tod" v-bind:key="item.id">
      {{ item.text }}
    </li>
  </div>
</template>
<script>
  export default {
    name: "compAlizee",
    props:{
      tod: {
        id: Number,
        text: String
      }
    }
  }
</script>

<style scoped>

</style>
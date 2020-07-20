<template>
    <v-badge v-if="getNumberOfCompound>0"
             color="secondary"
             overlap
             :content="getNumberOfCompound"
    />
</template>

<script>
    import { mapGetters } from 'vuex'
    export default {
        name: "CompoundsBadge",
        props: {
            textItem: ''
        },
        computed: {
            ...mapGetters([
                'getNumberOfCompound'
            ])
        }
    }
</script>

<style scoped>

</style>
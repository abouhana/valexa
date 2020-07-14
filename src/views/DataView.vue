<template>
    <div class="black--text">
        <vue-excel-editor v-model="jsondata">
            <vue-excel-column field="user"   label="User" />
            <vue-excel-column field="name"   label="Name" />
            <vue-excel-column field="phone"  label="Contact" />
            <vue-excel-column field="gender" label="Gender" />
            <vue-excel-column field="age"    label="Age" />
            <vue-excel-column field="birth"  label="Date Of Birth" />
        </vue-excel-editor>
    </div>
</template>

<script>
    import { HotTable } from '@handsontable/vue';

    export default {
        name: 'data-view',
        data: function() {
            return {
                jsondata: [
                    {user: '', name: '', phone: '', gender: 'M', age: 25, birth: '1997-07-01'},
                    {user: '', name: '', phone: '', gender: 'M', age: 20, birth: '1999-11-12'},
                    {user: '', name: '', phone: '', gender: 'M', age: 19, birth: '2000-06-11'},
                    {user: '', name: '', phone: '', gender: 'F', age: 22, birth: '2002-08-01'},
                    {user: '', name: '', phone: '', gender: 'M', age: 29, birth: '1990-09-01'},
                    {user: '', name: '', phone: '', gender: 'M', age: 29, birth: '1990-09-01'}
                ]
            }
        },
        components: {
            HotTable
        }
    }
</script>

<style scoped>
</style>
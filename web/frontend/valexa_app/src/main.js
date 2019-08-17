import Vue from 'vue'
import App from './App.vue'
import axios from "axios"

Vue.config.productionTip = false

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';


new Vue({
  render: h => h(App),
}).$mount('#app')

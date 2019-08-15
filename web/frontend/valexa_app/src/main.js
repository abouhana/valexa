import Vue from 'vue'
import App from './App.vue'
import axios from "axios"
import Cookies from "js-cookie"

Vue.config.productionTip = false

axios.defaults.headers.common['X-CSRFTOKEN'] = Cookies.get('csrftoken');
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';


new Vue({
  render: h => h(App),
}).$mount('#app')

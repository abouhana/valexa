import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';

import VueProgress from 'vue-progress-path'

Vue.use(VueProgress)
Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')

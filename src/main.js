import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';

import VueProgress from 'vue-progress-path'

Vue.use(VueProgress)
Vue.config.productionTip = false
Vue.config.devtools = process.env.NODE_ENV === 'development';

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')

import Vue from 'vue'
import App from './App.vue'
import axios from "axios"
import VeeValidate from "vee-validate"

Vue.config.productionTip = false;

VeeValidate.Validator.extend('file', (value, [otherValue]) => {
  // do something and finally return an object like this one:
  return {
    valid: false, // or false
    data: {
      required: true // or false
    }
  };
}, {
  computesRequired: true
})

Vue.use(VeeValidate, {
  classes: true
});

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';


new Vue({
  render: h => h(App),
}).$mount('#app')

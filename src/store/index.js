import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const index = new Vuex.Store({
  state: {
    valexa_is_valid: false,
    validation_pass: 0,
    validation_fail: 0,
    validation_current_name: "",

  },
  mutations: {
    increment_validation_fail (state) {
      state.validation_fail++
    },
    increment_validation_pass (state) {
      state.validation_pass++
    },
    set_validation_current_name (state, name) {
      state.validation_current_name = name
    },
    set_valexa_is_valid_true (state) {
      state.valexa_is_valid = true
    }

  }
})

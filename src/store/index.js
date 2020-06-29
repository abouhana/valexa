import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    valexaIsValid: false,
    validationTotalNumber: 0,
    validationCurrentNumber: 0,
    validationPass: 0,
    validationFail: 0,
    validationCurrentName: "",
    validationDescription: [],
    validationStatus: "",
    validationAccepted: "",

    loadBalancerProc: 0
  },
  mutations: {
    incrementValidationFail (state) {
      state.validationFail++
    },
    incrementValidationPass (state) {
      state.validationPass++
    },
    incrementValidationCurrentNumber (state) {
      state.validationCurrentNumber++
    },
    setValidationTotalNumber (state, number) {
      state.validationTotalNumber = number
    },
    setValidationCurrentName (state, name) {
      state.validationCurrentName = name
    },
    setValexaIsValidTrue (state) {
      state.valexaIsValid = true
    },
    setValidationStatus (state, status) {
      state.validationStatus = status
    },
    addValidationDescription (state, validationStatus) {
      state.validationDescription.push({
        name: state.validationCurrentName,
        status: validationStatus
      })
    },
    setValidationAccepted (state) {
      state.validationAccepted = true
    },

    incrementLoadBalancerProc (state) {
      state.loadBalancerProc++
    },

    decrementLoadBalancerProc (state) {
      state.loadBalancerProc--
    }

  },
  getters: {
    getValidationProgress: state => {
      return state.validationCurrentNumber / state.validationTotalNumber
    }
  }
})

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default {
  state: {
    valexaIsValid: false,
    validationTotalNumber: 0,
    validationCurrentNumber: 0,
    validationPass: 0,
    validationFail: 0,
    validationCurrentName: "",
    validationDescription: [],
    validationStatus: "",
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
        status: validationStatustatus
      })
    }
  },
  getters: {
    getValidationProgress: state => {
      return state.validationCurrentNumber / state.validationTotalNumber
    }
  }
}

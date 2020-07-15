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
    validationAccepted: false,

    loadBalancerProc: 0,

    listOfProfile: {},
    listOfProfileCompleted: false,

    stateLoading: {
      validation: false,
      backend: false,
      profileTable: false
    },
    loadingStatus: {
      validation: 'done',
      backend: ''
    },

    enteredData: { validation: [], calibration: [] },

    profileParams: {},

    modelParams: {}
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
    setLoadingStatus (state, part) {
      state.loadingStatus[part.name] = part.status
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
    },

    makeProfileList (state, profilesData) {
      Vue.set(state.listOfProfile, profilesData.id, profilesData)
    },

    setStateLoading (state, part) {
      state.stateLoading[part.name] = part.status
    },

    finishListOfProfile (state) {
      state.listOfProfileCompleted = true
    },

    resetListOfProfile (state) {
      state.listOfProfile = {}
      state.listOfProfileCompleted = false
    },

    setEnteredData (state, enteredValue) {
      state.enteredData[enteredValue.dataType] = enteredValue.tableData
    },

    addProfileParam (state, parameter) {
      state.profileParams[parameter.parameter] = {
        description: parameter.description,
        type: parameter.type,
        group: parameter.group,
        default: parameter.default,
        optional: parameter.optional
      }
    },

    addModelParam (state, parameter) {
      state.modelParams[parameter.name] = {
        formula: parameter.formula,
        weight: parameter.weight,
        minPoints: parameter.minPoints
      }
    }
  },

  getters: {
    getValidationProgress: state => {
      return state.validationCurrentNumber / state.validationTotalNumber
    },

    getProfilesTable: state => {
      return Object.values(state.listOfProfile)
    },

    getProfile: (state) => (id) => {
      return state.listOfProfile[id]
    },

    getEnteredData: (state) => (dataType) => {
      return state.enteredData[dataType]
    },

    isSomethingLoading: (state) => {
      return Object.values(state.stateLoading).includes(true)
    }
  }
})

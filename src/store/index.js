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
    validationAccepted: true,

    loadBalancerProc: 0,

    listOfProfile: {},
    listOfProfileCompleted: false,

    stateLoading: {
      validation: false,
      backend: false,
      profiles: false
    },
    loadingStatus: {
      validation: '',
      backend: ''
    },

    tableConfig: {},
    enteredData: {},

    profileParams: {},
    profileGenerationParams: {},

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

    setEnteredData (state, parameter) {
      state.enteredData[parameter.compound][parameter.dataType] = parameter.tableData
    },

    emptyEnteredData (state, parameter) {
      state.enteredData[parameter.compound][parameter.dataType] = []
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

    addProfileGenerationParam (state, parameter) {
      state.profileGenerationParams[parameter.name] = parameter.value
    },

    addModelParam (state, parameter) {
      state.modelParams[parameter.name] = {
        formula: parameter.formula,
        weight: parameter.weight,
        minPoints: parameter.minPoints
      }
    },

    setTableConfig (state, parameter) {
      state.tableConfig[parameter.compound][parameter.dataType] = parameter.data
    },

    renameData (state, parameter) {
      if (parameter.newName !== parameter.oldName) {
        Vue.set(state.enteredData, parameter.newName,state.enteredData[parameter.oldName])
        Vue.set(state.tableConfig, parameter.newName, state.tableConfig[parameter.oldName])
        delete state.enteredData[parameter.oldName]
        delete state.tableConfig[parameter.oldName]
      }
    },

    initCompoundData (state, parameter) {
      Vue.set(state.enteredData, parameter.compound, { validation: [], calibration: []})
      Vue.set(state.tableConfig, parameter.compound, {
        validation: {
          numberOfLevel: 3,
          numberOfSeries: 3,
          numberOfRep: 3,
          numberOfSupp: 0
        },
        calibration: {
          numberOfLevel: 3,
          numberOfSeries: 3,
          numberOfRep: 3,
          numberOfSupp: 0
        }
      })
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

    getEnteredData: (state) => (parameter) => {
      return state.enteredData[parameter.compound][parameter.dataType]
    },

    isSomethingLoading: (state) => {
      return Object.values(state.stateLoading).includes(true)
    },

    getTableConfig: (state) => (parameter) => {
      return state.tableConfig[parameter.compound][parameter.dataType]
    },

    getNumberOfCompound: (state) => {
      console.log(Object.keys(state.enteredData))
      return Object.keys(state.enteredData).length
    }
  }
})

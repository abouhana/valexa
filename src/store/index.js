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

    compounds: {},
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
      Vue.set(state.compounds[parameter.compound].data, parameter.dataType, parameter.tableData)
    },

    emptyEnteredData (state, parameter) {
      Vue.set(state.compounds[parameter.compound].data, parameter.dataType, [])
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
      Vue.set(state.compounds[parameter.compound].tableConfig, parameter.dataType, parameter.data)
    },

    renameData (state, parameter) {
      if (parameter.newName !== parameter.oldName) {
        Vue.set(state.compounds, parameter.newName, state.compounds[parameter.oldName])
        Vue.delete(state.compounds, parameter.oldName)
      }
    },

    initCompoundData (state, parameter) {
      Vue.set(state.compounds, parameter.compound, {
        data: {validation: [], calibration: []},
        tableConfig: {
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
        }
      })
    },

    deleteCompoundData (state, parameter) {
      Vue.delete(state.compounds, parameter.name)
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
      return state.compounds[parameter.compound].data[parameter.dataType]
    },

    isSomethingLoading: (state) => {
      return Object.values(state.stateLoading).includes(true)
    },

    getTableConfig: (state) => (parameter) => {
      return state.compounds[parameter.compound].tableConfig[parameter.dataType]
    },

    getNumberOfCompound: (state) => {
      return Object.keys(state.compounds).length
    },

    getListOfCompound: (state) => {
      return Object.keys(state.compounds)
    }
  }
})

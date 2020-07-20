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
    listOfProfileCompleted: true,

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
    settings: {
      default: { appliesTo: [] }
    },

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
      if (parameter.type.includes('bool')) {
        Vue.set(state.settings.default, parameter.parameter, JSON.parse(parameter.default.toLowerCase()))
      } else {
        Vue.set(state.settings.default, parameter.parameter, JSON.parse(parameter.default))
      }
    },

    addProfileGenerationParam (state, parameter) {
      state.profileGenerationParams[parameter.name] = parameter.value
    },

    addModelParam (state, parameter) {
      Vue.set(state.modelParams, parameter.name, {
        formula: parameter.formula,
        weight: parameter.weight,
        minPoints: parameter.minPoints
      })
    },

    setTableConfig (state, parameter) {
      Vue.set(state.compounds[parameter.compound].tableConfig, parameter.dataType, parameter.data)
    },

    renameCompoundData (state, parameter) {
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
        },
        setting: 'default',
        hasCalibration: true
      })
      state.settings.default.appliesTo.push(parameter.compound)
    },

    deleteCompoundData (state, parameter) {
      Vue.delete(state.compounds, parameter.name)
    },

    removeCalibrationFromCompound (state, parameter) {
      Vue.delete(state.compounds[parameter.compound].data, 'calibration')
      Vue.delete(state.compounds[parameter.compound].tableConfig, 'calibration')
      state.compounds[parameter.compound].hasCalibration = false
    },

    addCalibrationFromCompound (state, parameter) {
      Vue.set(state.compounds[parameter.compound].data, 'calibration', [])
      Vue.set(state.compounds[parameter.compound].tableConfig, 'calibration', {
            numberOfLevel: 3,
            numberOfSeries: 3,
            numberOfRep: 3,
            numberOfSupp: 0
          })
      state.compounds[parameter.compound].hasCalibration = true
    },

    initSettings (state, parameter) {
      Vue.set(state.settings, parameter.name, JSON.parse(JSON.stringify(state.settings.default)))
      state.settings[parameter.name].appliesTo = []
    },

    deleteSettings (state, parameter) {
      Vue.delete(state.settings, parameter.name)
    },

    renameSettings (state, parameter) {
      if (parameter.newName !== parameter.oldName && parameter.newName !== 'default' && parameter.oldName !== 'default') {
        Vue.set(state.settings, parameter.newName, state.settings[parameter.oldName])
        Vue.delete(state.settings, parameter.oldName)
      }
    },

    setSettingsValue (state, parameter) {
      Vue.set(state.settings[parameter.name], parameter.setting, parameter.value)
    },

    addModelNameToDefaultSetting (state) {
      Vue.set(state.settings.default, 'model_to_test', Object.keys(state.modelParams))
    },

    moveCompoundToSetting (state, parameter) {
      let currentSetting = state.compounds[parameter.compound].setting
      let compoundIndex = state.settings[currentSetting].appliesTo.indexOf(parameter.compound)

      state.compounds[parameter.compound].setting = parameter.setting
      state.settings[parameter.setting].appliesTo.push(parameter.compound)
      state.settings[currentSetting].appliesTo.splice(compoundIndex, 1)
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
    },

    getNumberOfSettings: (state) => {
      return Object.keys(state.settings).length
    },

    getListOfSettings: (state) => {
      return Object.keys(state.settings)
    },

    getSettingsValue: (state) => (parameter) => {
      return state.settings[parameter.name][parameter.setting]
    },

    getAvailableModelsName: (state) => {
      return Object.keys(state.modelParams)
    },

    getSettingForCompound: (state) => (parameter) => {
      console.log(JSON.stringify(parameter))
      console.log(JSON.stringify(state.compounds[parameter.compound].setting))
      console.log(JSON.stringify(state.settings[state.compounds[parameter.compound].setting]))
      console.log(JSON.stringify(state.settings[state.compounds[parameter.compound].setting][parameter.setting]))
      return state.settings[state.compounds[parameter.compound].setting][parameter.setting]
    },

    checkIfCompoundHasCalibration: (state) => (parameter) => {
      return state.compounds[parameter.compound].hasCalibration
    }
  }
})

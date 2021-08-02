import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)
function initialState () {
  return {
    SELECTED_APP: 'carts',
    SCATTERPLOT:[],
    SELECTED_PROJECT: 'tsne',
    LOAD_B: false,
    LOG_ID:null,
  }
}
export const store = new Vuex.Store({
  strict: true,
  state: initialState,
  mutations: {
  
    updateLOG_ID(state, newValue){
      state.LOG_ID = newValue
    },
    updateSELECTED_APP(state, newValue){
      state.SELECTED_APP = newValue
    },
    updateSCATTERPLOT(state, newValue){
        state.SCATTERPLOT = newValue
    },
    pushSCATTERPLOT(state,newValue){
      state.SCATTERPLOT.push(newValue)
    },
    sliceSCATTERPLOT(state){
      state.SCATTERPLOT.pop()
    },
    updateSELECTED_PROJECT(state, newValue){
        state.SELECTED_PROJECT = newValue
    },
    updateLOAD_B(state, newValue){
        state.LOAD_B = newValue
    },

  },
  getters: {
    SELECTED_APP: state => state.SELECTED_APP,
    SCATTERPLOT: state => state.SCATTERPLOT,
    SELECTED_PROJECT: state => state.SELECTED_PROJECT,
    LOAD_B: state => state.LOAD_B,
    LOG_ID: state => state.LOG_ID
  }
})
import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)
function initialState () {
  return {
    SELECTED_APP: [],
   
  }
}
export const store = new Vuex.Store({
  strict: true,
  state: initialState,
  mutations: {
    updateSELECTED_APP(state, newValue){
      state.SELECTED_APP = newValue
    }
  },
  getters: {
    SELECTED_APP: state => state.SELECTED_APP
  }
})
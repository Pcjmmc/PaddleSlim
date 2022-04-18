import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    'version': '',
    'appid': '',
    'appname': ''
  },
  mutations: {
    changeVersion (state, version) {
        state.version = version
    },
    changeAppid (state, appid) {
      state.appid = appid
    },
    changeAppName (state, appname) {
      state.appname = appname
    },
    removeCurrentApp (state) {
      state.appname = ''
      state.appid = ''
    }
  }
})

export default store

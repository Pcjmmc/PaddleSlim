import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie'

Vue.use(Vuex)

const store = new Vuex.Store({
  // 初始化app实例
  state: {
    'version': Cookies.get('version', ''),
    'appid': Cookies.get('appid', ''),
    'appname': Cookies.get('appname', '')
  },
  mutations: {
    changeVersion (state, version) {
      state.version = version;
    },
    changeAppid (state, appid) {
      state.appid = appid;
    },
    changeAppName (state, appname) {
      state.appname = appname;
    },
    removeCurrentApp (state) {
      state.appname = '';
      state.appid = '';
    }
  }
})

export default store

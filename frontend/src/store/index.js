import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie';

Vue.use(Vuex)

const store = new Vuex.Store({
  // 初始化app实例
  state: {
    'version': '',
    'appid': Cookies.get('appid', 1),
    'appname': Cookies.get('appname', '飞桨核心框架')
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

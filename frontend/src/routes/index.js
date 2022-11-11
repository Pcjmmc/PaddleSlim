import Vue from 'vue';
import VueRouter from 'vue-router';
import {ROUTES} from '../common/router.js';
import Cookies from 'js-cookie';
import api from '../api/index';

Vue.use(VueRouter)

const router = new VueRouter({
  routes: ROUTES
})

router.beforeEach((to, from, next) => {
  let hasAppId = Boolean(Cookies.get('appid'));
  let username = Cookies.get('username');
  let userid = Cookies.get('userid');
  if (!username || !userid) {
    // 首次登录或者是登出之后，再更新用户信息到表内部
    api.get('/ce/check')
    .then(function (response) {
      if (to.name !== 'AppStore' && !hasAppId) {
        Cookies.set('appid', 1);
        Cookies.set('appname', '飞桨核心框架');
        next();
      } else {
        next();
      }
    })
    .catch(function (error) {
      console.log(error);
    });
  } else if (to.name !== 'AppStore' && !hasAppId) {
    Cookies.set('appid', 1);
    Cookies.set('appname', '飞桨核心框架');
    next();
  } else {
    next()
  }
})
export default router

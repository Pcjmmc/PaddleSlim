import Vue from 'vue'
import VueRouter from 'vue-router'
import {ROUTES} from '../common/router.js'
import Cookies from 'js-cookie'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: ROUTES
})

router.beforeEach((to, from, next) => {
  let hasAppId = Boolean(Cookies.get('appid'));
  if (to.name !== 'AppStore' && !hasAppId) {
    next('/app_store')
  } else {
    next()
  }
})
export default router

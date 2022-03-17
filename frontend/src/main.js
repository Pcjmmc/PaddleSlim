import Vue from 'vue';
import router from './routes';
import iView from 'view-design';
import echarts from "echarts";
import VueCookie from 'vue-cookie';
import 'view-design/dist/styles/iview.css';
import VueVideoPlayer from 'vue-video-player';
import VueCookies from 'vue-cookies';
import App from './App';
import VueJsonPretty from 'vue-json-pretty';

Vue.prototype.$echarts = echarts;
Vue.use(iView);
Vue.use(VueCookie);
Vue.use(VueVideoPlayer);
Vue.use(VueCookies);
Vue.component('vue-json-pretty', VueJsonPretty);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  template: '<App/>',
  components: {App},
  data: {
    Hub: new Vue() // 事件传递中心
  }
});

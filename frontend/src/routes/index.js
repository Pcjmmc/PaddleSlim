import Vue from 'vue';
import VueRouter from 'vue-router';
import ApiDetails from '../components/ApiDetails.vue';
import Content from '../components/Content.vue';
import CommitDetails from '../components/CommitDetails.vue'
import JobsManage from '../components/Config/JobsManage.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  base: __dirname,
  routes: [
    { // 主页
      path: '/:paddle?',
      component: Content
    },
    { // API 配置
      path: '/paddle/frame-api-detail',
      name: 'ApiDetails',
      component: ApiDetails
    },
    { // API 配置
      path: '/paddle/commit-detail',
      name: 'CommitDetails',
      component: CommitDetails
    },
    { // API 配置
      path: '/paddle/release/:tag/:version',
      name: 'Content',
      component: Content
    },
    { // API 配置
      path: '/paddle/release/:version?',
      name: 'Content',
      component: Content
    },
    { // API 配置
      path: '/paddle/config/jobs',
      name: 'JobsManage',
      component: JobsManage
    }
  ]
});

export default router;

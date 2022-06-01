import Vue from 'vue';
// import VueRouter from 'vue-router';
import ApiDetails from '../components/ApiDetails.vue';
import Content from '../components/Content.vue';
import Main from '../components/Main.vue';
import CommitDetails from '../components/CommitDetails.vue';
import JobsManage from '../components/Config/JobsManage.vue';
import Model from '../components/Model.vue';
import AppStore from '../components/AppStore/index.vue';
import FuncDetail from '../components/FuncDetail.vue';
import Compile from '../components/Compile.vue';

// Vue.use(VueRouter);
export const ROUTES = [
    { // 应用选择
      path: '/app_store',
      name: 'AppStore',
      component: AppStore
    },
    { // 主页
      path: '/:paddle?',
      component: Main,
      children: [
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
          path: '/paddle/integration/:tag/:version',
          name: 'Content',
          component: Content
        },
        { // API 配置
          path: '/paddle/integration/:version?',
          name: 'Content',
          component: Content
        },
        { // API 配置
          path: '/paddle/config/jobs',
          name: 'JobsManage',
          component: JobsManage
        },
        { // API 配置
          path: '/paddle/detail/model',
          name: 'model',
          component: Model
        },
        { // API 配置
          path: '/paddle/detail/frame',
          name: 'FuncDetail',
          component: FuncDetail
        },
        { // API 配置
          path: '/paddle/detail/compile',
          name: 'Compile',
          component: Compile
        }
      ]
    }
  ]
// const router = new VueRouter({
//   base: __dirname,
//   routes: [
//     { // 应用选择
//       path: '/app_store',
//       name: 'app_store',
//       component: AppStore
//     },
//     { // 主页
//       path: '/:paddle?',
//       component: Content
//     },
//     { // API 配置
//       path: '/paddle/frame-api-detail',
//       name: 'ApiDetails',
//       component: ApiDetails
//     },
//     { // API 配置
//       path: '/paddle/commit-detail',
//       name: 'CommitDetails',
//       component: CommitDetails
//     },
//     { // API 配置
//       path: '/paddle/release/:tag/:version',
//       name: 'Content',
//       component: Content
//     },
//     { // API 配置
//       path: '/paddle/release/:version?',
//       name: 'Content',
//       component: Content
//     },
//     { // API 配置
//       path: '/paddle/config/jobs',
//       name: 'JobsManage',
//       component: JobsManage
//     },
//     { // API 配置
//       path: '/paddle/detail/model',
//       name: 'model',
//       component: Model
//     }
//   ]
// });

// export default router;

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
import Benchmark from '../components/Benchmark.vue';
import SingleReport from '../components/SingleReport.vue';
import Publish from '../components/publish/Publish.vue';
import TestService from '../components/Framework/testService.vue';
import TaskDetail from '../components/Framework/TaskDetail.vue';
import BinarySearch from '../components/BinarySearch.vue';
import ReleaseVersion from '../components/Config/ReleaseVersion.vue';

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
      // 默认跳到集测页
      redirect: '/paddle/integration',
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
        // { // API 配置
        //   path: '/paddle/integration/:tag/:version',
        //   name: 'Content',
        //   component: Content
        // },
        { // API 配置
          path: '/paddle/integration',
          name: 'Content',
          component: Content
        },
        // { // API 配置
        //   path: '/paddle/integration/:version?',
        //   name: 'Content',
        //   component: Content
        // },
        { // API 配置
          path: '/paddle/config/jobs',
          name: 'JobsManage',
          component: JobsManage
        },
        { // API 配置
          path: '/paddle/config/version',
          name: 'VersionManage',
          component: ReleaseVersion
        },
        { // API 配置
          path: '/paddle/config/binary',
          name: 'binarySearch',
          component: BinarySearch
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
        },
        { // API 配置
          path: '/paddle/op-benchmark',
          name: 'Benchmark',
          component: Benchmark
        },
        { // API 配置
          path: '/paddle/test/history',
          name: 'single_report',
          component: SingleReport
        },
        { // API 配置
          path: '/paddle/publish',
          name: 'publish',
          component: Publish
        },
        { // API 配置
          path: '/paddle/framework/service',
          name: 'PaddleService',
          component: TestService
        },
        { // API 配置
          path: '/paddle/framework/detail',
          name: 'PaddleDetail',
          component: TaskDetail
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

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
import BinarySearch from '../components/BinarySearch.vue';
import ReleaseVersion from '../components/Config/ReleaseVersion.vue';
import PaddleService from '../components/PTS/PaddleService.vue';
import TestService from '../components/PTS/TestService.vue';
import SingleDetail from '../components/PTS/SingleDetail.vue';
import Demand from '../components/Requirement/Demand.vue';
import ReqirementDetail from '../components/Requirement/ReqirementDetail.vue';
import SummaryResult from '../components/NewConclusion/SummaryResult';
import ApiBenchmarkService from '../components/ApiBenchmark/ApiBenchmarkService.vue';
import ApiBenchmarkBaseReport from '../components/ApiBenchmark/Report.vue';
import ModelBenchmarkHomePage from '../components/ModelBenchmark/homePage.vue';
import CompetitiveProductComparison from '../components/Benchmark/CompetitiveProductComparison.vue';

// Vue.use(VueRouter);
export const ROUTES = [
    { // 应用选择
      path: '/app_store',
      name: 'AppStore',
      component: AppStore
    },
    { // 其他应用主页
      path: '/default',
      name: 'Default',
      component: Main
    },
    { // Paddle核心框架主页
      path: '/:paddle?',
      component: Main,
      // 默认跳到集测页
      redirect: '/paddle/integration/',
      children: [
        { // API 配置
          path: '/paddle/frame-api-detail',
          name: 'ApiDetails',
          component: ApiDetails
        },
        { // API 配置
          path: '/paddle/commit-detail/:version',
          name: 'CommitDetails',
          component: CommitDetails
        },
        { // API 配置
          path: '/paddle/integration/',
          name: 'Content',
          component: Content
        },
        { // API 配置
          path: '/paddle/integration-summary/:version',
          name: 'SummaryResult',
          component: SummaryResult
        },
        { // API 配置
          path: '/paddle/integration/:version',
          name: 'ContentVersion',
          component: Content
        },
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
          path: '/paddle/requirement',
          name: 'PaddleDemand',
          component: Demand
        },
        { // API 配置
          path: '/paddle/test/framework-service',
          name: 'TestService',
          component: TestService
        },
        { // API 配置
          path: '/paddle/test/compile-service',
          name: 'PaddleService',
          component: PaddleService
        },
        { // API 配置
          path: '/paddle/test/SingleDetail/:jid',
          name: 'SingleDetail',
          component: SingleDetail
        },
        { // API 配置
          path: '/paddle/requirement/ReqDetail/:reqid',
          name: 'ReqDetails',
          component: ReqirementDetail
        },
        { // API 配置
          path: '/paddle/test/history',
          name: 'single_report',
          component: SingleReport
        },
        { // API 配置
          path: '/paddle/publish/:version',
          name: 'PublishVersion',
          component: Publish
        },
        { // API 配置
          path: '/paddle/benchmark/apiBenchmark',
          name: 'ApiBenchmarkService',
          component: ApiBenchmarkService
        },
        { // API 配置
          path: '/paddle/benchmark/apiBenchmark/report/:id&:id1',
          name: 'ApiBenchmarkBaseReport',
          component: ApiBenchmarkBaseReport
        },
        { // API 配置
          path: '/paddle/benchmark/modelBenchmark/homepage',
          name: 'homePage',
          component: ModelBenchmarkHomePage
        },
        {
          path: '/paddle/benchmark/compare/torch',
          name: 'CompetitiveProductComparison',
          component: CompetitiveProductComparison
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

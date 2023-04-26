<template>
<div>
  <div class="all-line-row">
    <!--
    <div v-if="allSteps.integration !== undefined && allSteps.integration.flag">
      <intergration
        :repoinfo="repoinfo"
        :bugdata="bugdata"
        :processdata="processdata"
      >
      </intergration>
    </div>
    <div v-else-if="allSteps.regression !== undefined && allSteps.regression.flag">
      <regression :data="bugdata"></regression>
    </div>
    <div v-else-if="allSteps.createtag !== undefined && allSteps.createtag.flag">
      <intergration
        :repoinfo="repoinfo"
        :bugdata="bugdata"
        :processdata="processdata"
      >
      </intergration>
    </div>
    <div v-else-if="allSteps.release !== undefined && allSteps.release.flag">
      <regression :data="bugdata"></regression>
    </div>
    !-->
    <div>
      <intergration
        :repoinfo="repoinfo"
        :processdata="processdata"
        :summary="summary"
      >
      </intergration>
    </div>
  </div>
</div>
</template>

<script>
import Cookies from 'js-cookie';
import api from '../api/index';
import { ReleaseVersionUrl, DevelopVersionUrl } from '../api/url.js';
import BaseInfo from './BaseInfo.vue';
import { CheckVersion } from '../util/help.js';
import Intergration from './Intergration.vue';
import Regression from './Regression.vue';

export default {
  data: function () {
    return {
      tagForm: {
        branch: '',
        tagName: '',
        commit: ''
      },
      repoinfo: {},
      processdata: {},
      summary: [],
      allSteps: {},
      // integrationdata: {
      //   data: []
      // },
      bugdata: []
    }
  },
  mounted: function () {
    this.SyncSelected();
    this.initData();
    this.getData();
  },
  watch: {
    versionName: function () {
      // 如果变化，选项变化则同步到路由中
      let data = {
        name: 'ContentVersion',
        params: {
          version: this.versionName ? this.versionName.replace('/', '-') : this.versionName
        }
      };
      // 如果有query则最近进去
      if (this.$route.query.tab) {
        if (['progress', 'risk', 'conclusion'].includes(this.$route.query.tab)) {
          let tmp = this.$route.query.tab;
          data.query = {tab: tmp};
        }
      }
      this.$router.push(data).catch(error => {
        if (error.name !== 'NavigationDuplicated') {
          throw error;
        }
      });
      this.getData();
    },
    $route() {
      if (this.$route.params.version) {
        let rs = CheckVersion(this.$route.params.version);
        let _version = rs ? this.$route.params.version.replace('-', '/') : this.$route.params.version;
        Cookies.set('version', _version);
        Cookies.set('ver', _version);
        this.$store.commit('changeVersion', _version);
      }
    }
  },
  components: {
    BaseInfo,
    Intergration,
    Regression
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    SyncSelected() {
      let rs = CheckVersion(this.$route.params.version);
      let tmpVer = rs ? this.$route.params.version.replace('-', '/') : this.$route.params.version;
      let _version = this.$route.params.version ? tmpVer : this.$store.state.version;
      let data = {
        name: 'ContentVersion',
        params: {
          version: _version.replace('/', '-')
        }
      };
      if (this.$route.query.tab) {
        if (['progress', 'risk', 'conclusion'].includes(this.$route.query.tab)) {
          let tmp = this.$route.query.tab;
          data.query = {tab: tmp};
        }
      } else {
        data.query = {tab: 'progress'};
      }
      this.$store.commit('changeVersion', _version);
      Cookies.set('version', _version);
      Cookies.set('ver', _version);
      this.$router.push(data).catch(error => {
        if (error.name !== 'NavigationDuplicated') {
          throw error;
        }
      });
    },
    async getData() {
      // 判断参数如果参数中有tag，则name=version；如果没有，则name=release+version
      let tmpVersion = this.versionName;
      let _params = {
        'version': tmpVersion,
        'appid': Cookies.get('appid')
      };
      let code = null;
      let data = null;
      let version = null;
      if (tmpVersion === 'develop') {
        let res = await api.get(DevelopVersionUrl, _params);
        code = res.code;
        data = res.data;
        version = res.version;
      } else {
        let res = await api.get(ReleaseVersionUrl, _params);
        code = res.code;
        data = res.data;
        version = res.version;
      }
      // 获取任务进展数据
      // 获取bug数据
      // console.log("code", code)
      if (parseInt(code) == 200) {
        this.repoinfo = data.repo_info;
        this.tagForm.branch = this.repoinfo.branch;
        this.processdata = data.process_data;
        this.summary = data.summary;
      } else {
        this.repoinfo = {};
        this.$Message.error({
          content: '请求出错: ' + version,
          duration: 30,
          closable: true
        })
      }
    },
    async selectDate() {
      this.getData();
    },
    initDate() {
      let day1 = new Date();
      day1.setDate(day1.getDate() - 1);
      return day1;
    },
    initData() {
      this.tagForm.tagName = '';
      this.tagForm.commit = '';
    },
    handleReset(auto) {
      // this.allSteps.createtag.flag = false;
      this.initData(auto);
    },
    async handleSubmit(auto) {
      await this.getData();
      // 成功或失败，都需要关闭窗口
      this.initData(auto);
    },
    // showModal(key, item) {
    //   let status = item.status;
    //   if (status == 'wait') {
    //     this.$Message.info({
    //       content: "请先保证任务通过并修复卡片，请稍后再试。。。",
    //       duration: 3,
    //       closable: true
    //     });
    //   } else {
    //     for (let ky in this.allSteps) {
    //       this.allSteps[ky].flag = false;
    //     }
    //     if (key == 'createtag') {
    //       if (status == 'process') {
    //         this.allSteps[key].flag = true;
    //       }
    //     } else {
    //       this.allSteps[key].flag = true;
    //     }
    //   }
    // },
    jumper(row) {
      let _params = {
        'tid': row.tid,
        'tname': row.project_name,
        'build_type_id': row.build_type_id
      };
      _params = Object.assign(_params, row);
      // 打开新的页面展示详情
      const { href } = this.$router.resolve({name: row.task_type, query: _params});
      window.open(href, '_blank');
    }
  }
};
</script>

<style scoped>
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
</style>

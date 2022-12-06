<template>
  <div class="all-line-row">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="编译"
        name="progress"
      >
        <div style="margin-bottom:1%;">
          <Table
            align="center"
            border
            :columns="columns"
            :data="summary"
          >
          </Table>
        </div>
        <div>
          <el-tabs
            type="card"
            v-model="childname"
            @tab-click="clickChildTab"
          >
            <el-tab-pane
              :key="index"
              :label="item"
              :name="item"
              v-for="(item, index) in publishOriginList"
            >
              <publish-test :data="integrationdata"></publish-test>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-tab-pane>
      <el-tab-pane
        label="发布"
        name="publish"
      >
      <upload-result> </upload-result>
      </el-tab-pane>
   </el-tabs>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import api from '../../api/index';
import { ScenesUrl, PublishJobUrl, PublishProcessUrl } from '../../api/url.js';
import CaseBase from '../CommonUtil/CaseBase.vue';
import publishTest from './publishTest.vue';
import uploadResult from './uploadResult.vue';

export default {
  name: 'Publish',
  data: function () {
    return {
      childname: 'pypi/bos',
      summary: [],
      integrationdata: [],
      columns: [
        {
          title: '阶段',
          key: 'step',
          align: 'center'
        },
        {
        title: '总数 ｜ 成功 ｜失败',
        key: 'casedetail',
        align: 'center',
        render: (h, params) => {
          return h(CaseBase, {
            props: {
              total: params.row.total,
              failed: params.row.failed,
              succeed: params.row.succeed,
              needSucceed: true,
              xs: 2
            },
            style: {
              fontSize: '14px'
            }
          });
        }
        }
      ],
      publishOriginList: []
    };
  },
  watch: {
    version: function () {
      let data = {
        name: 'PublishVersion',
        params: {
          version: this.version
        }
      };
      // 如果有query则最近进去
      if (this.$route.query.tab) {
        if (['progress', 'publish'].includes(this.$route.query.tab)) {
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
      this.getSummary();
    },
    $route() {
      let _version = this.$route.params.version;
      Cookies.set('version', _version);
      this.$store.commit('changeVersion', _version);
    }
  },
  mounted: function () {
    this.SyncSelected();
    this.getScenesList();
    this.getSummary();
    this.getData();
  },
  components: {
    publishTest,
    uploadResult
  },
  computed: {
    version: {
      get() {
        return this.$store.state.version;
      }
    },
    tabName() {
      let tmp = 'progress';
      if (this.$route.query.tab) {
        if (['progress', 'publish'].includes(this.$route.query.tab)) {
          tmp = this.$route.query.tab;
        }
        this.$router.replace({query: {tab: tmp}}).catch(error => {
          if (error.name !== 'NavigationDuplicated') {
            throw error;
          }
        });
      }
      return tmp;
    }
  },
  methods: {
    SyncSelected() {
      let _version = this.$route.params.version ? this.$route.params.version : this.$store.state.version;
      this.$store.commit('changeVersion', _version);
      Cookies.set('version', _version);
      let data = {
        name: 'PublishVersion',
        params: {
          version: _version
        }
      };
      if (this.$route.query.tab) {
        if (['progress', 'publish'].includes(this.$route.query.tab)) {
          let tmp = this.$route.query.tab;
          data.query = {tab: tmp};
        }
      }
      this.$router.push(data).catch(error => {
        if (error.name !== 'NavigationDuplicated') {
          throw error;
        }
      });
    },
    clickTab(name) {
      if (this.$route.query.tab) {
        let query = {tab: name};
        this.$router.replace({query: query}).catch(error => {
          if (error.name !== 'NavigationDuplicated') {
            throw error;
          }
        });
      }
    },
    clickChildTab(item) {
      this.childname = item.name;
      this.integrationdata = [];
      this.getData();
    },
    async getScenesList() {
      const {code, data, message} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.publishOriginList = data.publishOriginList;
      } else {
        this.publishOriginList = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getSummary() {
      let params = {
        version: this.version,
        step: 'publish',
        task_type: 'compile',
        tag: this.tag,
        appid: Cookies.get('appid')
      };
      const {code, data, message} = await api.get(PublishProcessUrl, params);
      if (parseInt(code, 10) === 200) {
        this.summary = data;
      } else {
        this.summary = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      // 根据需求实时获取; 后台根据version获取到计划tag
      if (!this.version) {
        return;
      }
      let params = {
        version: this.version,
        step: 'publish',
        task_type: 'compile',
        release_source: this.childname,
        tag: this.tag,
        appid: Cookies.get('appid')
      };
      // console.log('requests data', params);
      const {code, data, message} = await api.get(PublishJobUrl, params);
      if (parseInt(code, 10) === 200) {
        this.integrationdata = data;
      } else {
        this.integrationdata = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
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


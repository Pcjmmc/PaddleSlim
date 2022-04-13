<template>
  <div>
    <Tabs :value="tabName" v-on:on-click="clickTab">
      <TabPane
        label="进度"
        name="10001"
        icon="ios-list-box"
      >
        <div>
          <div>
            <Divider
            orientation="left"
            style="font-size: 0.5em;font-style: italic;margin-top: 0.1px"
          >
          测试进度及信息 </Divider>
          </div>
          <div style="margin-bottom: 2%">
            <base-info :repoinfo="repoinfo" :processdata="processdata"> </base-info>
          </div>
          <Tabs
            type="card"
            :value="childname"
            v-on:on-click="clickChildTab"
          >
            <TabPane
            :label="item.desc"
            :name="item.key"
            v-for="(item, index) in taskTypeList"
            >
              <integration-test
                :data="integrationdata"
                :tag="repoinfo.tag"
                :versionid="repoinfo.version_id"
                :versionname="repoinfo.name"
                :secondtype="sendTypeList[item.key]"
              >
              </integration-test>
            </TabPane>
          </Tabs>
        </div>
      </TabPane>
      <TabPane
        label="风险"
        name="10002"
        icon="ios-bug"
      >
        <bug-fix ref="mychild" :datas="bugdata"></bug-fix>
      </TabPane>
    </Tabs>
  </div>
</template>

<script>
import api from '../api/index';
import { ScenesUrl, ReleaseJobUrl } from '../api/url.js';
import IntegrationTest from './IntegrationTest.vue';
import BugFix from './BugFix.vue';
import ApiCoverage from './ApiCoverage.vue';
import BaseInfo from './BaseInfo.vue';

export default {
  props: {
    bugdata: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    repoinfo: {
      type: Object,
      default: null
    },
    processdata: {
      type: Object,
      default: null
    }
  },
  data: function () {
    return {
      tabName: '10001',
      childname: 'compile',
      taskTypeList: [],
      sendTypeList: {},
      integrationdata: [],
      routeParams: this.$route.params,
      version: ''
    };
  },
  watch: {
    $route() {
      this.routeParams = this.$route.params;
      this.initData();
      this.getData();
    }
  },
  mounted: function () {
    this.getScenesList();
    this.getData();
  },
  components: {
    BaseInfo,
    ApiCoverage,
    BugFix,
    IntegrationTest
  },
  computed: {
  },
  methods: {
    clickTab(name) {
      this.tabName = name;
      // console.log(this.tabName);
      this.$nextTick(function () {
        this.$refs.mychild.getStatusFilters();
      });
    },
    clickChildTab(name) {
      this.childname = name;
      // console.log('this child name', this.childname);
      this.getData();
    },
    initData() {
      if ('tag' in this.routeParams) {
        this.version = this.routeParams.version;
      } else {
        // 如果version是空
        this.version = 'release/' + this.routeParams.version;
      }
    },
    async getScenesList() {
      const {code, data, msg} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.taskTypeList = data.taskTypeList;
        this.sendTypeList = data.sendTypeList;
      } else {
        this.taskTypeList = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      // 根据需求实时获取
      if ('tag' in this.routeParams) {
        this.version = this.routeParams.version;
      } else {
        // 如果version是空
        this.version = 'release/' + this.routeParams.version;
      }
      let params = {
        'version': this.version,
        'task_type': this.childname
      };
      // console.log('根据要求获取数据', params);
      const {code, data, msg} = await api.get(ReleaseJobUrl, params);
      if (parseInt(code, 10) === 200) {
        // console.log('data is', data);
        this.integrationdata = data;
      } else {
        this.integrationdata = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    }
  }
};
</script>

<style scoped>
</style>

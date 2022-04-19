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
          <div style="margin-bottom: 2%;">
            <h5 style="margin-left: 2%;"> 集测整体进展 </h5>
            <Table
              size="small"
              align=center
              border
              :columns="columns"
              :data="taskTypeList"
              style="margin-left: 2%;margin-right: 2%;"
            >
            </Table>
          </div>
          <el-tabs
            type="card"
            v-model="childname"
            @tab-click="clickChildTab"
            style="margin-left: 1%;"
          >
            <el-tab-pane
            :label="item.desc"
            :name="item.key"
            :key="index"
            v-for="(item, index) in taskTypeList"
            >
              <integration-test
                :data="integrationdata"
                :tag="repoinfo.tag"
                :versionid="repoinfo.version_id"
                :versionname="repoinfo.name"
                :secondtype="sendTypeList[item.key]"
                :tabname="childname"
              >
              </integration-test>
            </el-tab-pane>
          </el-tabs>
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
import Cookies from 'js-cookie';
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
      columns: [
      {
        title: '分类',
        key: 'desc',
        align: 'center'
      },
      {
        title: '状态',
        key: 'status',
        align: 'center'
      },
      {
        title: '运行用例数',
        key: 'case',
        align: 'center'
      }
    ]
    };
  },
  watch: {
    version: function () {
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
    version: {
      get () {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    clickTab(name) {
      this.tabName = name;
      // console.log(this.tabName);
      this.$nextTick(function () {
        this.$refs.mychild.getStatusFilters();
      });
    },
    clickChildTab(item) {
      this.childname = item.name;
      this.integrationdata = [];
      // 将选中的tab标记成蓝色
      // console.log('this child name', this.childname);
      this.getData();
    },
    async getScenesList() {
      const {code, data, msg} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.taskTypeList = data.taskTypeList;
        console.log("this.taskTypeList", this.taskTypeList);
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
      let params = {
        'version': this.version,
        'task_type': this.childname,
        'appid': Cookies.get('appid')
      };
      const {code, data, msg} = await api.get(ReleaseJobUrl, params);
      if (parseInt(code, 10) === 200) {
        if (JSON.stringify(data) === '{}') {
          this.integrationdata = [];
        } else {
          this.integrationdata = data;
          // console.log('this.childname', this.childname);
          // console.log('this.integrationdata', this.integrationdata);
        }
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

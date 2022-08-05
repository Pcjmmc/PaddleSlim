<template>
  <div>
    <Tabs :value="tabName" v-on:on-click="clickTab">
      <TabPane
        label="进度"
        name="10001"
        icon="ios-list-box"
      >
        <div style="margin-bottom: 2%;">
          <Table
              size="small"
              align="center"
              border
              :columns="columns"
              :data="summary"
              style="margin-left: 2%;margin-right: 2%;"
          >
          </Table>
        </div>
        <div>
          <el-tabs
            type="card"
            style="margin-left: 1%;"
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
      </TabPane>
      <TabPane
        label="上传"
        name="10002"
        icon="md-analytics"
      >
      </TabPane>
   </Tabs>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import api from '../../api/index';
import { ScenesUrl, PublishJobUrl } from '../../api/url.js';
import CaseBase from '../CommonUtil/CaseBase.vue';
import publishTest from './publishTest.vue';

export default {
  data: function () {
    return {
      tabName: '10001',
      childname: 'pypi',
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
      this.getData();
    }
  },
  mounted: function () {
    this.getScenesList();
    this.getSummary();
    this.getData();
  },
  components: {
    publishTest
  },
  computed: {
    version: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    clickTab(name) {
      this.tabName = name;
      // console.log(this.tabName);
    },
    clickChildTab(item) {
      this.childname = item.name;
      this.integrationdata = [];
      this.getData();
    },
    async getScenesList() {
      const {code, data, msg} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.publishOriginList = data.publishOriginList;
      } else {
        this.publishOriginList = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    async getSummary() {
      this.summary = [
        {
          step: '编译',
          total: 100,
          succeed: 50,
          failed: 2
        },
        {
          step: '验证',
          total: 100,
          succeed: 4,
          failed: 1
        },
        {
          step: '发布',
          total: 100,
          succeed: 3,
          failed: 0
        }
      ];
    },
    async getData() {
      // 根据需求实时获取; 后台根据version获取到计划tag
      let params = {
        version: this.version,
        step: 'publish',
        task_type: 'compile',
        origin: this.childname,
        tag: this.tag,
        appid: Cookies.get('appid')
      };
      // console.log('requests data', params);
      const {code, data, msg} = await api.get(PublishJobUrl, params);
      if (parseInt(code, 10) === 200) {
        this.integrationdata = data;
        this.integrationdata = [
          {
            system: 'Linux',
            data: [
              {
                tname: 'cuda10.2-cudnn7.6.5-mkl-gcc8.2-avx-py36',
                test_step: 0,
                status: '进行中'
              },
              {
                tname: 'cuda10.2-cudnn7.6.5-mkl-gcc8.2-avx-py36',
                test_step: 1,
                status: '失败'
              }
            ]
          }
        ];
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

<style>
.el-tabs__item.is-active {
  color: blue;
  background-color:rgb(69, 190, 238);
}
</style>

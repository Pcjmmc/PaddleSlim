<template>
  <div>
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="进度"
        name="progress"
      >
        <div>
          <div style="margin-bottom: 1%;">
            <base-info :repoinfo="repoinfo" :processdata="processdata"> </base-info>
          </div>
          <div style="margin-bottom: 1%;">
            <Table
              align=center
              :columns="columns"
              :data="summary"
            >
            </Table>
          </div>
          <el-tabs
            type="card"
            v-model="childname"
            @tab-click="clickChildTab"
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
                :latestcommittime="repoinfo.latest_commit_time"
                :versionid="repoinfo.version_id"
                :versionname="repoinfo.name"
                :secondtype="sendTypeList[item.key]"
                :tabname="childname"
              >
              </integration-test>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-tab-pane>
      <el-tab-pane
        label="风险"
        name="risk"
      >
        <bug-fix
          ref="mychild"
          :tag="repoinfo.tag"
          :tasktypelist="taskTypeList"
        ></bug-fix>
      </el-tab-pane>
      <el-tab-pane
        label="结论"
        name="conclusion"
      >
        <conclusion
          ref="mychild2"
          :tasktypelist="taskTypeList"
          :tag="repoinfo.tag"
          :branch="repoinfo.branch"
        ></conclusion>
      </el-tab-pane>
    </el-tabs>
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
import CircleBase from './CommonUtil/CircleBase.vue';
import CaseBase from './CommonUtil/CaseBase.vue';
import Conclusion from './Result/Conclusion.vue';

export default {
  props: {
    repoinfo: {
      type: Object,
      default: null
    },
    processdata: {
      type: Object,
      default: null
    },
    summary: {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      childname: 'compile',
      taskTypeList: [],
      sendTypeList: {},
      integrationdata: [],
      columns: [
      {
        title: '阶段',
        key: 'task_type',
        align: 'center',
        render: (h, params) => {
          return h('div', {
            style: {
              fontSize: '14px'
            }
          }, params.row.task_type);
        }
      },
      {
        title: '状态',
        key: 'status',
        align: 'center',
        render: (h, params) => {
          let ret = [];
          if (params.row.status.toLowerCase() === 'passed') {
            ret.push(
              h('Icon', {
                  props: {
                    type: 'md-checkmark-circle',
                    color: 'green',
                    size: '35'
                  }
                }
              )
            );
          } else if (params.row.status.toLowerCase() === 'failed') {
            ret.push(
              h('Icon', {
                  props: {
                    type: 'md-close-circle',
                    color: 'red',
                    size: '35'
                  }
                }
              )
            );
          } else {
            ret.push(
              h(CircleBase, {
                  props: {
                    percent: params.row.percent
                  },
                  style: {
                    fontSize: '14px'
                  }
                }
              )
            );
          }
        return h('div', ret);
        }
      },
      {
       title: '运行用例数',
       key: 'case',
       align: 'center',
        render: (h, params) => {
          return h(CaseBase, {
            props: {
              total: params.row.total,
              failed: params.row.failed
            },
            style: {
              fontSize: '14px'
            }
          });
        }
      }
      // {
      //   title: '运行用例数',
      //   key: 'case',
      //   align: 'center',
      //   render: (h, params) => {
      //     let ret = []
      //     ret.push(
      //       h(
      //         'span',
      //         {
      //           style: {
      //             marginRight: '5px',
      //             marginBottom: '3px',
      //             width: '50px',
      //             color: params.row.failed ? 'red' : 'green',
      //             fontSize: '14px'
      //           }
      //         }, params.row.total)
      //     )
      //     ret.push(
      //       h(
      //         'span',
      //         {
      //           style: {
      //             marginRight: '5px',
      //             marginBottom: '3px',
      //             width: '50px'
      //           }
      //         }, '|')
      //     )
      //     ret.push(
      //       h(
      //         'span',
      //         {
      //           style: {
      //             marginRight: '5px',
      //             marginBottom: '3px',
      //             width: '50px',
      //             color: params.row.failed ? 'red' : 'green',
      //             fontSize: '14px'
      //           }
      //         }, params.row.failed)
      //     )
      //     return h('div', ret)
      //   }
      // }
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
    IntegrationTest,
    Conclusion
  },
  computed: {
    version: {
      get() {
        return this.$route.params.version ? this.$route.params.version : this.$store.state.version;
      }
    },
    tabName: {
      get() {
        let tmp = 'progress';
        if (this.$route.query.tab) {
          if (['progress', 'risk', 'conclusion'].includes(this.$route.query.tab)) {
            tmp = this.$route.query.tab;
          }
          this.$router.replace({query: {tab: tmp}}).catch(error => {
            if (error.name !== 'NavigationDuplicated') {
              throw error;
            }
          });
        }
        return tmp;
      },
    set(val) {
    }
    }
  },
  methods: {
    clickTab(name) {
      let tmpname = name.name;
      if (this.$route.query.tab) {
        let query = {tab: tmpname};
        this.$router.replace({query: query}).catch(error => {
          if (error.name !== 'NavigationDuplicated') {
            throw error;
          }
        });
      }
      this.$nextTick(function () {
        if (name === 'conclusion') {
          this.$refs.mychild2.getData();
        } else {
          this.$refs.mychild.getbugdata();
          this.$refs.mychild.getStatusFilters();
        }
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
      const {code, data, message} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.taskTypeList = data.taskTypeList;
        // console.log("this.taskTypeList", this.taskTypeList);
        this.sendTypeList = data.sendTypeList;
      } else {
        this.taskTypeList = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      // 根据需求实时获取
      if (!this.version) {
        return;
      }
      let params = {
        'version': this.version,
        'task_type': this.childname,
        'appid': Cookies.get('appid')
      };
      const {code, data, message} = await api.get(ReleaseJobUrl, params);
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
</style>

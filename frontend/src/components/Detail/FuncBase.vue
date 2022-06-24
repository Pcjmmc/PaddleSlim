<template>
    <div style="padding: 0px 20px 0px 20px">
      <Card :bordered="false" class="center-card-s">
        <p
          slot="title"
          style="text-align: center;font-size: 1.4em;"
          v-if="index==0"
        >
          <Icon type="ios-information-circle" size="20"></Icon>
          {{ "任务信息概述" }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          任务名: {{ $route.query.tname }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          repo信息: {{ $route.query.repo }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          commit信息: {{ $route.query.commit_id }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          commit提交时间: {{ changeTimestamp($route.query.commit_time) }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          分支信息: {{ $route.query.branch }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;"
          v-if="index==0"
        >
          执行时间: {{ changeTimestamp($route.query.created) }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;color: red"
          v-if="index==0 && $route.query.status.toLowerCase()=='failed'"
        >
          执行结果: {{ $route.query.status }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;color: green"
          v-else-if="index==0"
        >
          执行结果: {{ $route.query.status }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.0em;color: red"
          v-if="$route.query.status.toLowerCase()=='failed' && index==0"
        >
          原因: {{ getErrorReason($route.query.exit_code) }}
        </p>
      </Card>
      <Card :bordered="false" class="center-card-s">
        <p slot="title" style="text-align: center;font-size: 1.2em;">
          {{ secondarytype }}
        </p>
        <Table
          border
          :columns="detailColumns"
          :data="summarydata"
          style="margin-right: 1%"
        >
        </Table>
      </Card>
      <Card
        v-if="failedData.length > 0"
        :bordered="false"
        class="center-card-s"
      >
        <p slot="title" style="text-align: center;font-size: 1.2em;">
          {{ "失败case" }}
        </p>
        <Scroll
          :height="contentHeight"
          :on-reach-bottom="addDataArr"
          :loading-text="loadingText"
        >
          <frame-detail-base
            :data="failedData"
            :columns="Columns"
          >
          </frame-detail-base>
        </Scroll>
      </Card>
      <Card
        v-if="succeedData.length > 0"
        :bordered="false"
        class="center-card-s"
      >
        <p slot="title" style="text-align: center;font-size: 1.2em;">
          {{ "成功case" }}
        </p>
        <Scroll
          :height="contentHeight2"
          :on-reach-bottom="addDataArr"
          :loading-text="loadingText2"
        >
          <frame-detail-base
            :data="succeedData"
            :columns="Columns"
          >
          </frame-detail-base>
        </Scroll>
      </Card>
      <Modal
        v-model="ShowDetail"
        title="用例详情"
        width="1000px"
      >
        <vue-json-pretty
          :data="ErrorDetail"
        >
        </vue-json-pretty>
        <div slot="footer">
        </div>
      </Modal>
    </div>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import { dateFmt, timestampToTime } from '../../util/help.js';
import frameDetailBase from '../base/frameDetailBase.vue';
export default {
  props: {
    'detail': {
      type: Object,
      default: function () {
        return null;
      }
    },
    'secondarytype': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'summarydata': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    index: {
      type: [Number],
      default: function () {
        return null;
      }
    }
  },
  data: function () {
    return {
      ShowDetail: false,
      ErrorDetail: {},
      failedData: [],
      succeedData: [],
      contentHeight2: 100,
      contentHeight: 100,
      loadingText: '加载中',
      loadingText2: '加载中',
      num: 10,
      detailColumns: [
        {
          title: '总数',
          key: 'total',
          align: 'center'
        },
        {
          title: '失败case数',
          key: 'failed_num',
          align: 'center'
        },
        {
          title: '成功case数',
          key: 'passed_num',
          align: 'center'
        }
      ],
      Columns: [
        {
          title: '文件名',
          key: 'fullName',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
                style: {
                  marginRight: '5px'
                }
              }, params.row.fullName.split('#')[0])
            ]);
          }
        },
        {
          title: 'case名',
          key: 'name',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            const { status } = params.row;
            return h('div', [
              h('Tag', {
              props: {
                color: this.setColor(status)
              }
              }, status)
            ]);
          }
        },
        {
          title: '注释',
          minWidth: 200,
          key: 'description',
          align: 'center'
        },
        {
          title: '详情',
          key: 'statusDetails',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'primary'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleEdit(params.row);
                  }
                }
              }, '详情')
            ]);
          }
        }
      ],
      ExpandColumns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            // console.log('params', params.row.data);
            return h(frameDetailBase, {
                props: {
                  data: params.row.data,
                  columns: this.Columns
                }
            });
          }
        },
        {
          title: '阶段名',
          key: 'step',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center'
        }
      ]
    };
  },
  mounted: function () {
    // console.log('data', this.detail);
    this.addDataArr();
    this.initHeight();
  },
  components: {
    VueJsonPretty,
    frameDetailBase
  },
  computed: {
    allSourceFailed() {
      return this.detail.failed_data;
    },
    allSourceSuccess() {
      return this.detail.succeed_data;
    }
  },
  methods: {
    getErrorReason(exit_code) {
      switch (parseInt(exit_code, 10)) {
        case 0:
          return '成功';
        case 2:
          return 'CE框架失败';
        case 3:
          return '模型yaml书写错误';
        case 4:
          return 'Lite模型优化失败';
        case 5:
          return '未录入任务';
        case 7:
          return '编译失败';
        case 8:
          return 'case失败';
        case 63:
          return '克隆代码失败';
        case 125:
          return '启动容器失败';
        case 127:
          return 'tc没有执行权限';
        case 137:
          return 'tc任务取消';
        default:
          return '未知';
      }
    },
    changeTimestamp(timestamp, offset = 8) {
      if (timestamp) {
        let date = timestampToTime(timestamp, offset);
        let dt = dateFmt(date, 'yyyy-MM-dd hh:mm:ss');
        return dt;
      } else {
        return '';
      }
    },
    handleEdit(row) {
      this.ShowDetail = true;
      this.ErrorDetail = row;
    },
    initHeight() {
      let max_len1 = this.failedData.length;
      if (max_len1 > 0) {
        if (max_len1 <= 5) {
          this.contentHeight = (100 - (max_len1 - 1) * 10) * max_len1;
        } else if (max_len1 < 10) {
          this.contentHeight = 80 * max_len1;
        } else {
          this.contentHeight = 500;
        }
      }
      let max_len = this.succeedData.length;
      if (max_len > 0) {
        if (max_len <= 5) {
          this.contentHeight2 = (100 - (max_len - 1) * 10) * max_len;
        } else if (max_len < 10) {
          this.contentHeight2 = 80 * max_len;
        } else {
          this.contentHeight2 = 500;
        }
      }
    },
    addDataArr() {
      let max_len1 = Object.keys(this.allSourceFailed).length;
      if (max_len1 > 0) {
        let i = 0;
        max_len1 = max_len1 > this.num ? this.num : max_len1;
        for (let vd in this.allSourceFailed) {
          if (i < max_len1 && this.allSourceFailed[vd]) {
            this.failedData.push(this.allSourceFailed[vd]);
            this.allSourceFailed[vd] = null;
            delete this.allSourceFailed[vd];
            i = i + 1;
          } else {
            break;
          }
        }
      }
      let max_len = Object.keys(this.allSourceSuccess).length;
      if (max_len > 0) {
        let j = 0;
        max_len = max_len > this.num ? this.num : max_len;
        for (let vd in this.allSourceSuccess) {
          if (j < max_len && this.allSourceSuccess[vd]) {
            this.succeedData.push(this.allSourceSuccess[vd]);
            this.allSourceSuccess[vd] = null;
            delete this.allSourceSuccess[vd];
            j = j + 1;
          } else {
            break;
          }
        }
      }
      if (max_len === 0) {
        this.loadingText2 = '加载完成';
      }
      if (max_len1 === 0) {
        this.loadingText = '加载完成';
      }
    },
    // separateData() {
    //   let succeedArray = [];
    //   let faliedArray = [];
    //   for (var idx = 0; idx < this.detail.length; idx++) {
    //     let item = this.detail[idx];
    //     if (!item.status) {
    //       continue;
    //     }
    //     if (item.status.toLowerCase() === 'broken') {
    //       item.status = 'failed';
    //     }
    //     if (item.status.toLowerCase() === 'failed') {
    //       faliedArray.push(item);
    //     } else {
    //       succeedArray.push(item);
    //     }
    //   }
    //   let result = {
    //     'succeedArray': [],
    //     'faliedArray': []
    //   };
    //   if (succeedArray.length > 0) {
    //     result.succeedArray = succeedArray;
    //   }
    //   if (faliedArray.length > 0) {
    //     result.faliedArray = faliedArray;
    //   }
    //   return result;
    // },
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'passed':
          return 'success';
        case 'failed':
          return 'error';
        default:
          return 'warning';
      }
    }
  }
};
</script>

<style scoped>
  .tips {
    color: #ff9900;
  }
  .all-line-row {
    margin-bottom: 0.5%;
    margin-left: 0.5%;
  }
  .scroll-cls {
    overflow-y: auto;
  }
  .center-card-s {
    width: 98%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 0.5%
  }
</style>

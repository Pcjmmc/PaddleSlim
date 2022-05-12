<template>
    <div style="padding: 0px 20px 0px 20px">
      <Card :bordered="false">
        <p
          slot="title"
          style="text-align: left;font-size: 1.3em;color: red"
          v-if="$route.query.status.toLowerCase()=='failed'"
        >
          {{ secondarytype }}: {{ $route.query.status }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.3em;color: green"
          v-else
        >
          {{ secondarytype }}: {{ $route.query.status }}
        </p>
        <p
          slot="title"
          style="text-align: left;font-size: 1.3em;color: red"
          v-if="$route.query.status.toLowerCase()=='failed'"
        >
          原因: {{ getErrorReason($route.query.exit_code) }}
        </p>
        <Card :bordered="false" class="center-card-s">
          <p slot="title" style="text-align: center;font-size: 1.2em;">
            {{ "整体情况" }}
          </p>
          <Table
            border
            :columns="detailColumns"
            :data="summarydata"
            style="margin-right: 2%"
          >
          </Table>
        </Card>
        <Card
          v-if="failedData.length > 0"
          :bordered="false"
          class="center-card-s"
        >
          <p slot="title" style="text-align: center;font-size: 1.2em;">
            {{ "失败的case详情" }}
          </p>
          <Table
            :columns="ExpandColumns"
            :data="failedData"
            style="margin-right: 2%"
            border
          ></Table>
        </Card>
        <Card
          v-if="succeedData.length > 0"
          :bordered="false"
          class="center-card-s"
        >
          <p slot="title" style="text-align: center;font-size: 1.2em;">
            {{ "成功case详情" }}
          </p>
            <Table
              :columns="ExpandColumns"
              :data="succeedData"
              style="margin-right: 2%"
              border
            ></Table>
        </Card>
      </Card>
      <Modal
        v-model="ShowDetail"
        title="错误详情"
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
      type: [Array],
      default: function () {
        return [];
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
    }
  },
  data: function () {
    return {
      ShowDetail: false,
      ErrorDetail: {},
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
            console.log('params', params.row.data);
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
    console.log('data', this.detail);
  },
  components: {
    VueJsonPretty
  },
  computed: {
    failedData() {
      const {faliedArray} = this.separateData();
      console.log('faliedArray', faliedArray);
      return faliedArray;
    },
    succeedData() {
      const {succeedArray} = this.separateData();
      return succeedArray;
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
    separateData() {
      let succeedArray = [];
      let faliedArray = [];
      for (var idx = 0; idx < this.detail.length; idx++) {
        let item = this.detail[idx];
        if (!item.status) {
          continue;
        }
        if (item.status.toLowerCase() === 'broken') {
          item.status = 'failed';
        }
        if (item.status.toLowerCase() === 'failed') {
          faliedArray.push(item);
        } else {
          succeedArray.push(item);
        }
      }
      let result = {
        'succeedArray': [],
        'faliedArray': []
      };
      if (succeedArray.length > 0) {
        result.succeedArray = [
          {'step': 'succeed case', 'status': 'Passed', 'data': succeedArray}
        ];
      }
      if (faliedArray.length > 0) {
        result.faliedArray = [
          {'step': 'failed case', 'status': 'Failed', 'data': faliedArray}
        ];
      }
      return result;
    },
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
  .center-card-s {
    width: 98%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 2%
  }
</style>

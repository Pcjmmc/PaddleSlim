<template>
  <div>
    <Card class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
          <Icon type="ios-information-circle" size="20"></Icon>
          {{ "任务信息概述" }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em; margin-top: 5%">
        任务名: {{ $route.query.tname }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: green"
        v-else
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        原因: {{ getErrorReason($route.query.exit_code) }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        repo信息: {{ $route.query.repo }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        commit信息: {{ $route.query.commit_id }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        分支信息: {{ $route.query.branch }}
      </p>
      <!--
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        <a :href="getTaskUrl()"> 任务链接</a>
      </p>
      -->
      <Table
        border
        :columns="detailColumns"
        :data="summaryData"
        style="margin-right: 2%"
      >
      </Table>
    </Card>
    <Card v-if="failedData.length > 0" class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon
          type="ios-close-circle"
          color="red"
          size="20"
        >
        </Icon>
        {{ "失败的case" }}
      </p>
      <div v-for="(item, index) in failedData">
        <model-base
          :model-name="item.model_name"
          :kpis="item.kpis"
          :status="item.status"
        ></model-base>
      </div>
    </Card>
    <Card v-if="succeedData.length > 0" class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon
            type="ios-checkmark-circle"
            color="green"
            size="20"
        ></Icon>
        {{ "成功的case" }}
      </p>
      <div v-for="(item, index) in succeedData">
        <model-base
          :model-name="item.model_name"
          :kpis="item.kpis"
          :status="item.status"
        ></model-base>
      </div>
    </Card>
  </div>
</template>

<script>
import api from '../api/index';
import { DetailUrl } from '../api/url.js';
import { dateFmt, timestampToTime } from '../util/help.js';
import ModelBase from './CommonUtil/ModelBase.vue';
export default {
  data: function () {
    return {
      summaryData: [],
      detail: {},
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
      ]
    };
  },
  mounted: function () {
    // console.log("$route.query", this.$route.query);
    this.getData();
  },
  components: {
    ModelBase
  },
  computed: {
    failedData() {
      const {failedData} = this.separateData();
      // console.log('failedData is', failedData);
      return failedData;
    },
    succeedData() {
      const {succeedData} = this.separateData();
      // console.log('succeedData is', succeedData);
      return succeedData;
    }
  },
  methods: {
    separateData() {
      let failedData = [];
      let succeedData = [];
      let tmp_detail = this.detail;
      Object.keys(tmp_detail).forEach(function (item) {
        switch (tmp_detail[item].status.toLowerCase()) {
          case 'passed':
            succeedData.push(Object.assign({'model_name': item}, tmp_detail[item]));
            break;
          case 'failed':
            failedData.push(Object.assign({'model_name': item}, tmp_detail[item]));
            break;
          default:
            break;
        }
      });
      return {'failedData': failedData,
              'succeedData': succeedData};
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
    async getData() {
      // console.log('params is', this.$route.query);
      let _params = {
        'tid': this.$route.query.tid,
        'build_id': this.$route.query.build_id,
        'task_type': this.$route.query.task_type,
        'secondary_type': this.$route.query.secondary_type
      };
      // 自己知道自己值传递了一个secondary_type
      const { code, data, message } = await api.get(DetailUrl, _params);
      if (message === 'success') {
        for (let key in data) {
          if (data.hasOwnProperty(key)) {
            this.detail = data[key].case_detail;
            this.summaryData = data[key].summary_data;
          }
        }
      } else {
        console.log('code: ', code);
        this.$Message.error({content: message || this.$trans('获取编译列表失败'), duration: 5, closable: true});
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
    width: 100%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 2%
  }
</style>

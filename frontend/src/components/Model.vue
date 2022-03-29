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
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        repo信息: {{ $route.query.repo }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        commit信息: {{ $route.query.commit_id }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        分支信息: {{ $route.query.branch }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        <a :href="getTaskUrl()"> 任务链接</a>
      </p>
      <Table
        :columns="detailColumns"
        :data="summaryData"
        style="margin-right: 2%"
      >
      </Table>
    </Card>
    <Card v-if="failedData.length > 0" class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon
          type="ios-close"
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
          :base-url="getCaseLogUrl()"
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
          :base-url="getCaseLogUrl()"
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
      detail: {},
      detailColumns: [
        {
          title: '失败case数',
          key: 'failed',
          align: 'center'
        },
        {
          title: '成功case数',
          key: 'succeed',
          align: 'center'
        },
        {
          title: '总数',
          key: 'total',
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
    summaryData() {
      const {summaryData} = this.separateData();
      return summaryData;
    },
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
      let summaryData = [];
      let failedData = [];
      let succeedData = [];
      let res = {
        'total': 0,
        'succeed': 0,
        'failed': 0
      };
      let tmp_detail = this.detail;
      Object.keys(tmp_detail).forEach(function (item) {
        res.total += 1;
        switch (tmp_detail[item].status.toLowerCase()) {
          case 'passed':
            res.succeed += 1;
            succeedData.push(Object.assign({'model_name': item}, tmp_detail[item]));
            break;
          case 'failed':
            res.failed += 1;
            failedData.push(Object.assign({'model_name': item}, tmp_detail[item]));
            break;
          default:
            break;
        }
      });
      summaryData.push(res);
      return {'summaryData': summaryData,
              'failedData': failedData,
              'succeedData': succeedData};
    },
    getTaskUrl() {
      let uri = 'http://paddle-ce.bcc-bdbl.baidu.com:8111/viewLog.html?buildId=' + this.$route.query.build_real_id + '&buildTypeId=' + this.$route.query.build_type_id + '&tab=buildLog';
      return uri;
    },
    getCaseLogUrl() {
      let url = 'http://paddle-ce.bcc-bdbl.baidu.com:8111/repository/download/' + this.$route.query.build_type_id +  '/' + this.$route.query.build_real_id + ':id' + '/log/';
      // console.log("url is", url)
      return url;
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
    async getData() {
      // console.log('params is', this.$route.query);
      let _params = {
        'tid': this.$route.query.tid,
        'build_id': this.$route.query.build_id,
        'task_type': this.$route.query.task_type
      };
      const { code, data, message } = await api.get(DetailUrl, _params);
      if (message === 'success') {
        this.detail = data;
        // console.log("this detail", this.detail);
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

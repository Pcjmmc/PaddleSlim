<template>
  <div>
    <div class="center-card-s">
      <Row style="margin-top: 1%;">
        <span> 任务ID: {{ jobinfo.id }}</span>
      </Row>
      <Row style="margin-top: 1%;" v-if="jobinfo.name">
        <span> 任务名: {{ jobinfo.name }} </span>
      </Row>
      <Row style="margin-top: 1%;">
        <span style="display:inline-block;width:95%;margin-bottom:1%;"> 环境配置: </span>
        <span
          style="display:inline-block;width:95%;margin-bottom:1%;"
        > {{ getDisplay(env) }}</span>
        <span style="display:inline-block;"> {{ env.type + ':' + env.value }}</span>
      </Row>
      <Row style="margin-top: 1%;" v-if="req">
        <span style="display:inline-block;width:95%;margin-bottom:1%;">
          <span> 关联需求: </span>
          <a href="javascript:void(0)" @click="jumper()">
            {{ req.desc }}
          </a>
        </span>
      </Row>
      <Row style="margin-top: 2%;">
        <Table
          border
          :columns="columns"
          :data="datas"
        ></Table>
      </Row>
    </div>
  </div>
</template>

<script>
import { FrameWorkJobDetail, FrameReportUrl } from '../../api/url.js';
import api from '../../api/index';
import { TestServerMap } from '../../util/common.js';

export default {
  name: 'SingleDetail',
  props: {},
  data: function () {
    return {
      req: {
        id: 3,
        desc: 'xxxx'
      },
      jobinfo: {
        id: this.$route.params.jid,
        name: ''
      },
      env: {},
      datas: [],
      columns: [
        {
          title: '测试项',
          key: 'mission',
          align: 'center',
          fixed: 'left'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Tag', {
                props: {
                  color: this.setColor(params.row.status)
                },
                style: {
                  width: '100px'
                }
              }, this.getStatus(params.row.status))
            ]);
          }
        },
        {
          title: '结果',
          key: 'result',
          align: 'center',
          width: '350px',
          render: (h, params) => {
            return h('div', [
              h('p', {
                style: {
                  color: '#9F35FF'
                }
              }, this.getDetail(params.row))
            ]);
          }
        },
        {
          title: '时间',
          key: 'create_time',
          align: 'center'
        },
        {
          title: '详细报告',
          key: 'report',
          align: 'center',
          fixed: 'right',
          width: '200px',
          render: (h, params) => {
            let bos_url = params.row.bos_url;
            let allure_report = params.row.allure_report;
            let ret = [];
            if (bos_url) {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.generateReport(params.row);
                      }
                    }
                  },
                  '生成报告'
                )
              );
            } else {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small',
                      disabled: true
                    },
                    style: {
                      marginRight: '5px'
                    }
                  },
                  '生成报告'
                )
              );
            }
            if (allure_report) {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.openReport(params.row);
                      }
                    }
                  },
                  '查看报告'
                )
              );
            } else {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small',
                      disabled: true
                    },
                    style: {
                      marginRight: '5px'
                    }
                  },
                  '查看报告'
                )
              );
            }
            return h(
              'div',
              {
                style: {
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'flex-start',
                  alignItems: 'flex-start'
                }
              },
              ret
            );
          }
        }
      ]
    };
  },
  mounted: function () {
    this.getDetails();
  },
  components: {
  },
  methods: {
    async getDetails() {
      let jid = this.$route.params.jid;
      let params = {
        id: jid
      };
      const {code, data, message} = await api.get(FrameWorkJobDetail, params);
      if (parseInt(code, 10) === 200) {
        // 塞到datas的detais 字段里面
        if (typeof data.compile === 'object') {
          let compile = data.compile;
          this.env = JSON.parse(compile.env);
        } else {
          this.env = {};
        }
        let mission = typeof data.mission === 'object' ? data.mission : {};
        this.jobinfo.name = data.descrption;
        this.jobinfo.id = data.id;
        // 将mission转换成想要的数据格式
        this.datas = this.getData(mission);
        // 构造一个假数据
        // this.datas = [
        //   {
        //     mission: this.getMissionName('external_api_function'),
        //     allure_report: 'http://paddletest.baidu-int.com:8333/211666182177_id_154',
        //     bos_url: 'https://paddle-qa.bj.bcebos.com/PTS/mission_result/mission_154/custom_op.tar',
        //     create_time: '2022-10-11 20:49:16',
        //     id: 154,
        //     result: '{"total": 12, "success": 12, "skip": 0, "failed": 0}',
        //     status: 'done'
        //   },
        //   {
        //     mission: this.getMissionName('op_function'),
        //     allure_report: 'http://paddletest.baidu-int.com:8333/211666182177_id_154',
        //     bos_url: 'https://paddle-qa.bj.bcebos.com/PTS/mission_result/mission_154/custom_op.tar',
        //     create_time: '2022-10-11 20:49:16',
        //     id: 155,
        //     result: '{"total": 10, "success": 10, "skip": 0, "failed": 0}',
        //     status: 'done'
        //   }
        // ];
      } else {
        this.jobinfo = {
          id: this.$route.params.jid,
          name: ''
        };
        this.env = {};
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    getData(dt) {
      let tmpData = [];
      for (let key in dt) {
        if (dt[key]) {
          let temp = {
            mission: this.getMissionName(key),
            status: dt[key].status,
            result: dt[key].result ? dt[key].result : {},
            create_time: dt[key].create_time,
            bos_url: dt[key].bos_url,
            allure_report: dt[key].allure_report,
            id: dt[key].id
          };
          tmpData.push(temp);
        }
      }
      return tmpData;
    },
    initData() {
      this.jobinfo = {
        id: this.$route.params.jid,
        name: ''
      };
      this.env = {};
      this.datas = [];
    },
    getMissionName(key) {
      return TestServerMap[key];
    },
    async generateReport(item) {
      let params = {
        bos_url: item.bos_url,
        id: item.id
      };
      console.log(params);
      const {code, data, message} = await api.post(FrameReportUrl, params);
      if (parseInt(code, 10) === 200) {
        item.allure_report = data.allure_report;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async openReport(item) {
      if (item.allure_report) {
        window.open(item.allure_report, '_blank');
      } else {
        this.$Message.error({
          content: '没有可查询报告，请先生成报告！',
          duration: 30,
          closable: true
        });
      }
    },
    getStatus(status) {
      switch (status.toLowerCase()) {
        case 'success':
          return '成功';
        case 'fail':
          return '失败';
        default:
          return status;
      }
    },
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'done':
          return 'success';
        case 'success':
          return 'success';
        case 'passed':
          return 'success';
        case 'pass':
          return 'success';
        case 'running':
          return 'primary';
        case 'warning':
          return 'warning';
        case 'error':
          return 'error';
        case 'fail':
          return 'error';
        case 'failed':
          return 'error';
        default:
          return 'error';
      }
    },
    jumper() {
      // 跳转到相应的需求页,自己的工作台 todo
      console.log('desc', this.req);
    },
    handleDetail() {
      console.log('查看allure 报告详情');
    },
    getDetail(row) {
      let result = row.result ? row.result.trim() : '';
      result = result.substr(1, result.length - 2);
      return result;
    },
    getDisplay(env) {
      let content_list = [];
      let key_list = ['os', 'branch', 'python', 'cuda'];
      for (let i = 0; i <= key_list.length; i++) {
        let key = key_list[i];
        if (env[key]) {
          content_list.push(env[key]);
        }
      }
      return content_list.join(' | ');
    }
  }
};
</script>
<style scoped>
.center-card-s {
  width: 95%;
  margin-left: 2%;
  margin-right: 2%;
  margin-top: 2%;
}
</style>

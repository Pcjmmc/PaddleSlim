<template>
  <div>
    <Card class="center-card-s">
      <Row style="margin-top: 1%;">
        <span> 任务名: {{ jobinfo.name }} </span>
        <span style="float:left;width:60%;margin-left: 2%;">
          <span style="float:left;width:60%;">
            <Steps
              :current="current"
              :status="stepStatus"
            >
              <Step title="编译"></Step>
              <Step title="测试任务"></Step>
            </Steps>
          </span>
        </span>
      </Row>
      <div style="margin-top: 1%;">
        <div> 环境配置: </div>
        <div>
          <Table
            border
            :columns="envcolumns"
            :data="envInfo"
          ></Table>
        </div>
      </div>
      <Card>
        <Row style="margin-top: 1%;" v-if="wheel">
          <span>编译产物: <a :href="wheel">{{ wheel }}</a>
            <Icon
              class="ivu-icon ivu-icon-ios-copy-outline copyBtn"
              type="ios-copy-outline"
              color="green"
              size="15"
              @click="copyData(wheel)"
            ></Icon>
          </span>
        </Row>
        <Row style="margin-top: 1%;" v-if="req">
          <span style="display:inline-block;width:95%;margin-bottom:1%;">
            <span> 关联需求: </span>
            <a href="javascript:void(0)" @click="jumper()">
              {{ req.desc }}
            </a>
          </span>
        </Row>
        <div style="margin-top: 1%;">
          <div v-if="datas.length === 0">
            <span>
              <span>测试项:</span>
              <Button
                disabled
                :key="index"
                v-for="(item, index) in selectedItems"
                style="width:150px;margin-left: 0.5%;"
              >
                {{ serverMap[item] }}
              </Button>
            </span>
          </div>
        </div>
      </Card>
      <!--
      <Row style="margin-top: 1%;">
        <span style="float:left;width:60%;">
          <span style="float:left;margin-right: 1%;">
            进度:
          </span>
          <span style="float:left;width:60%;">
            <Steps
              :current="current"
              :status="stepStatus"
            >
              <Step title="编译"></Step>
              <Step title="测试任务"></Step>
            </Steps>
          </span>
        </span>
      </Row>
      -->
    </Card>
    <Card
      class="center-card-s"
      v-if="datas.length > 0"
    >
      <div>
        <div>
          测试模块详情:
          <Table
            border
            :columns="columns"
            :data="datas"
          ></Table>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { FrameWorkJobDetail, FrameReportUrl, FrameMissionFailedUrl, FrameModuleConfigUrl, FrameMissionRerunUrl } from '../../api/url.js';
import api from '../../api/index';
import Clipboard from 'clipboard';
import Modal from '../ModalSimple/Modal.vue';

export default {
  name: 'SingleDetail',
  props: {},
  data: function () {
    return {
      serverMap: {},
      req: {
        id: 3,
        desc: 'xxxx'
      },
      jobinfo: {
        id: this.$route.params.jid,
        name: ''
      },
      wheel: null,
      current: -1,
      stepStatus: null,
      selectedItems: [],
      env: {},
      datas: [],
      envcolumns: [
        {
          title: '系统',
          key: 'os',
          align: 'center'
        },
        {
          title: 'CUDA',
          key: 'cuda',
          align: 'center'
        },
        {
          title: '分支',
          key: 'branch',
          align: 'center'
        },
        {
          title: 'python版本',
          key: 'python',
          align: 'center'
        },
        {
          title: '类型',
          key: 'type',
          align: 'center'
        },
        {
          title: '取值',
          key: 'value',
          align: 'center',
          render: (h, params) => {
            return h('Tooltip', {
              props: {
                placement: 'right',
                transfer: true
              }
            }, [
              h('div', {
                style: {
                  width: '100px',
                  overflow: 'hidden',
                  whiteSpace: 'nowrap',
                  textOverflow: 'ellipsis'
                }
              }, params.row.value),
              h('span', {
                slot: 'content',
                style: {
                  whiteSpace: 'normal',
                  wordBreak: 'break-all'
                }
              }, params.row.value)
            ]);
          }
        }
      ],
      columns: [
        {
          title: 'ID',
          key: 'id',
          align: 'center',
          fixed: 'left',
          width: '100px'
        },
        {
          title: '测试项',
          key: 'mission',
          align: 'center',
          width: '140px'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          width: '130px',
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
          title: '创建时间',
          key: 'create_time',
          width: '170px',
          align: 'center'
        },
        {
          title: '详细报告',
          key: 'report',
          align: 'center',
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
        },
        {
          title: '操作',
          key: 'operation',
          align: 'center',
          width: '190px',
          fixed: 'right',
          render: (h, params) => {
            let ret = [];
            ret.push(
              h(
                'Button',
                {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.setFailedStatus(params.row.id);
                    }
                  }
                },
                '标记异常'
              )
            );
            ret.push(
              h(
                'Button',
                {
                  props: {
                    icon: 'md-refresh-circle',
                    size: 'small'
                  },
                  style: {
                    'background-color': '#75C1C4',
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.rerunJob(params.row.id);
                    }
                  }
                },
                'rerun'
              )
            );
            return h(
              'div',
              ret
            );
          }
        }
      ]
    };
  },
  mounted: async function () {
    await this.getModuleConfig();
    await this.getDetails();
  },
  computed: {
    envInfo: {
      get() {
        let info = [];
        info.push(this.env);
        return info;
      }
    }
  },
  components: {
  },
  methods: {
    async getModuleConfig() {
      const {code, data, message} = await api.get(FrameModuleConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.serverMap = JSON.parse(data.module_mapping);
      } else {
        this.serverMap = {};
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async rerunJob(id) {
      Modal.confirm({
        title: '确认重跑？',
        onOk: async () => {
          let params = {
            id: id
          };
          const {code, message} = await api.post(FrameMissionRerunUrl, params);
          if (parseInt(code, 10) === 200) {
            await this.getDetails();
          } else {
            this.$Message.error({
              content: '请求出错: ' + message,
              duration: 30,
              closable: true
            });
          }
        }
      });
    },
    async getDetails() {
      let jid = this.$route.params.jid;
      let params = {
        id: jid
      };
      const {code, data, message} = await api.get(FrameWorkJobDetail, params);
      if (parseInt(code, 10) === 200) {
        // 塞到datas的detais 字段里面
        let status1 = data.compile.status;
        let status2 = data.status;
        this.getStepStatus(status1, status2);
        if (typeof data.compile === 'object') {
          let compile = data.compile;
          this.wheel = compile.wheel;
          this.env = JSON.parse(compile.env);
        } else {
          this.env = {};
        }
        let mission = typeof data.mission === 'object' ? data.mission : {};
        this.jobinfo.name = data.description;
        this.jobinfo.id = data.id;
        // 将mission转换成想要的数据格式
        this.datas = this.getData(mission);
      } else {
        this.jobinfo = {
          id: this.$route.params.jid,
          name: ''
        };
        this.env = {};
        this.datas = [];
        this.selectedItems = [];
        this.current = -1;
        this.stepStatus = null;
        this.wheel = null;
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
        this.selectedItems.push(key);
        if (dt[key]) {
          let temp = {
            mission: this.serverMap[key],
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
    getStepStatus(status1, status2) {
      if (status1 === 'running') {
        this.current = 0;
      } else if (status1 === 'done') {
        if (status2 === 'error') {
          this.current = 1;
          this.stepStatus = 'error';
        } else if (status2 === 'done') {
          this.current = 2;
        } else {
          this.current = 1;
        }
      } else if (status1 === 'error') {
        this.current = 0;
        this.stepStatus = 'error';
      }
    },
    initData() {
      this.jobinfo = {
        id: this.$route.params.jid,
        name: ''
      };
      this.env = {};
      this.datas = [];
      this.selectedItems = [];
      this.current = -1;
      this.stepStatus = null;
      this.wheel = null;
    },
    copyData(url) {
      let clipboard = new Clipboard('.copyBtn', {
          text: function (trigger) {
            clipboard.destroy();
            return url;
          }
      });
      clipboard.on('success', e => {
        this.$Message.success('复制成功~');
        e.clearSelection();
      });
      clipboard.on('error', e => {
        this.$Message.error('复制失败,请手动复制~');
      });
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
    async setFailedStatus(id) {
      Modal.confirm({
        title: '确认标记异常？',
        onOk: async () => {
          let params = {
            id: id
          };
          const {code, message} = await api.post(FrameMissionFailedUrl, params);
          if (parseInt(code, 10) === 200) {
            await this.getDetails();
          } else {
            this.$Message.error({
              content: '请求出错: ' + message,
              duration: 30,
              closable: true
            });
          }
        }
      });
    },
    getStatus(status) {
      switch (status.toLowerCase()) {
        case 'success':
          return '成功';
        case 'done':
          return '已完成';
        case 'fail':
          return '失败';
        case 'running':
          return '运行中';
        case 'error':
          return '异常';
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
          return 'warning';
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
      let result = row.result ? row.result : '';
      // result = result.substr(1, result.length - 2);
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

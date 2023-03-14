<template>
  <div>
    <Card class="center-card-s">
      <div slot="title" v-if="$route.params.jid">
       <p>
          <Row style="font-size:16px;">
            <Col>
              <h3>{{ jobinfo.name }}</h3>
            </Col>
          </Row>
        </p>
      </div>
      <div>
        <div> 环境配置: </div>
        <div style="margin-top: 1%;">
          <Table
            border
            :columns="envcolumns"
            :data="envInfo"
          ></Table>
        </div>
      </div>
      <Row style="margin-top: 2%;" v-if="wheel">
        <span>编译产物: </span>
          <span style="margin-top: 1%;">
            <a :href="wheel">{{ wheel }}</a>
            <Icon
              class="ivu-icon ivu-icon-ios-copy-outline copyBtn"
              type="ios-copy-outline"
              color="green"
              size="15"
              @click="copyData(wheel)"
            ></Icon>
          </span>
      </Row>
      <Row style="margin-top: 1%;" v-if="JSON.stringify(this.req) != '{}'">
        <span style="display:inline-block;width:95%;margin-bottom:1%;">
          <span> 关联IcafeId: </span>
          <a href="javascript:void(0)" @click="jumper(req.icafe_id)">
            {{ req.icafe_id }}
          </a>
        </span>
      </Row>
      <div style="margin-top:1%;font-size:14px;">
        <div v-if="datas.length === 0">
          <span>
            <div>待测试项:</div>
            <Button
              disabled
              :key="index"
              v-for="(item, index) in selectedItems"
              style="width:auto;margin-left:0.5%;margin-top:1%;"
            >
              {{ serverMap[item] }}
            </Button>
          </span>
        </div>
        <div v-else style="margin-top:2%;">
        测试模块详情:
        <div style="margin-top: 1%;">
          <Table
            :columns="columnsStep"
            :data="steps"
          ></Table>
        </div>
      </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { FrameWorkJobDetail, FrameReportUrl,
  FrameMissionFailedUrl, FrameModuleConfigUrl,
  FrameMissionRerunUrl, ReqInfoUrl
} from '../../api/url.js';
import api from '../../api/index';
import Clipboard from 'clipboard';
import Modal from '../ModalSimple/Modal.vue';
import childTable from './childTable.vue';

export default {
  name: 'SingleDetail',
  props: {
    jid: {
      type: [Number],
      default: function () {
        return null;
      }
    }
  },
  data: function () {
    return {
      columnsStep: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            if (params.row.step === "测试") {
              return h(childTable, {
                props: {
                  tableData: this.datas
                },
                on: {
                  getDetails: () => {
                    this.getDetails()
                  }
                }
              })
            }
          }
        },
        {
          title: '阶段',
          key: 'step',
          align: 'center',
          render: (h, params) => {
            if (params.row.step === "编译") {
              return h('div', [h('a', {
                attrs: {
                  href: 'javascript:void(0)'
                },
                on: {
                  click: () => {
                    this.openXly(params.row.info);
                  }
                }
              }, params.row.step)
              ]);
            } else {
              return h('div', {
              }, params.row.step);
            }
          }
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('tag', {
                props: {
                  color: this.setColor(params.row.status)
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
                h('font', {
                style: {
                  color: params.row.result ? 'red' : 'gray'
                }
                }, params.row.result ? params.row.result : '--')
            ]);
          }
        }
      ],
      steps: [
      ],
      serverMap: {},
      req: {},
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
          align: 'center',
          fixed: 'left'
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
          fixed: 'right',
          render: (h, params) => {
            return h('Tooltip', {
              props: {
                placement: 'right',
                transfer: true
              }
            }, [
              h('div', {
                style: {
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
      ]
    };
  },
  mounted: async function () {
    await this.getModuleConfig();
    await this.getInitData();
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
    childTable
  },
  methods: {
    async getInitData() {
      this.initData();
      await this.getDetails();
      await this.getReqInfo();
    },
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
    async getReqInfo() {
      let params = {
        test_id: this.$route.params.jid || this.jid
      };
      const {code, data, message} = await api.get(ReqInfoUrl, params);
      if (parseInt(code, 10) === 200) {
        this.req = data;
      } else {
        this.req = {};
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getDetails() {
      let jid = this.$route.params.jid || this.jid;
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
          id: this.$route.params.jid || this.jid,
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
      this.selectedItems = [];
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
            id: dt[key].id,
            description: dt[key].description,
            info: dt[key].info
          };
          tmpData.push(temp);
        }
      }
      return tmpData;
    },
    getStepStatus(status1, status2) {
      this.steps = [
        {
          step: '编译',
          status: status1,
          _disableExpand: true,
          result: ''
        },
        {
          step: '测试',
          status: status2,
          _expanded: true
        }
      ]
      // if (status1 === 'running') {
      //   this.current = 0;
      // } else if (status1 === 'done') {
      //   if (status2 === 'error') {
      //     this.current = 1;
      //     this.stepStatus = 'error';
      //   } else if (status2 === 'done') {
      //     this.current = 2;
      //   } else {
      //     this.current = 1;
      //   }
      // } else if (status1 === 'error') {
      //   this.current = 0;
      //   this.stepStatus = 'error';
      // }
    },
    initData() {
      this.jobinfo = {
        id: this.$route.params.jid || this.jid,
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
    jumper(key) {
      // 跳转到相应的需求页,自己的工作台 todo
      let url = `https://console.cloud.baidu-int.com/devops/icafe/issue/DLTP-${key}/show`;
      window.open(url, '_blank');
    },
    openXly(url) {
      if (url) {
        window.open(url, '_blank');
      } else {
        this.$Message.info({
          content: '下游任务没有回写任务地址!',
          duration: 5,
          closable: true
        });
      }
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
  width: 100%;
  font-size: 14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
</style>

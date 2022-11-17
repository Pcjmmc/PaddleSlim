<template>
  <div>
   <Card
      class="center-card-s"
    >
      <div>
        <Row style="margin-top: 1%;">
          <Col>
            需求title: {{ content.title }}
          </Col>
          <Col offset="1">
            RD: {{ content.rd_owner }}
          </Col>
          <Col offset="1">
            QA: {{ content.qa_owner }}
          </Col>
          <Col offset="1">
          Repo: {{ content.repo }}
          </Col>
          <Col offset="1">
          pr:
          <a href="javascript:void(0)" @click="jumper(content.pr)">
            {{ content.pr }}
          </a>
          </Col>
        </Row>
      </div>
    </Card>
   <Card
      class="center-card-s"
    >
      <div>
        <div>
        测试记录
          <Table
            border
            :columns="columns"
            :data="datas"
          ></Table>
        </div>
      </div>
    </Card>
    <Modal
      v-model="showApproveModa"
      title="确认结果"
      width="30%"
      v-on:on-cancel="handleReset"
    >
      <RadioGroup v-model="approve">
        <Radio label="pass">成功</Radio>
        <Radio label="fail">失败</Radio>
      </RadioGroup>
      <div slot="footer">
        <Button type="text" @click="handleReset">取消</Button>
        <Button type="primary" @click="handleSubmit">提交</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { dateFmt, timestampToTime } from '../../util/help.js';
import { RequriementDetailUrl, StartTestUrl, UserCheckUrl, AssociateBugUrl } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'ReqDetails',
  props: {},
  data: function () {
    return {
      userInfo: {
        identifyQA: false,
        username: Cookies.get('username')
      },
      content: null,
      showApproveModa: false,
      approve: 'pass',
      datas: [],
      columns: [
        {
          title: '测试任务ID',
          key: 'test_id',
          align: 'center',
          fixed: 'left'
        },
        {
          title: '测试任务状态',
          key: 'test_status',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Tag', {
                props: {
                  color: this.setColor(params.row.test_status)
                },
                style: {
                  width: '100px'
                }
              }, this.getStatus(params.row.test_status))
            ]);
          }
        },
        {
          title: '测试时间',
          key: 'created',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
              }, this.changeTimestamp(params.row.created))
            ]);
          }
        },
        {
          title: '测试结论',
          key: 'approve',
          align: 'center'
        },
        {
          title: '测试项详情',
          key: 'report',
          align: 'center',
          render: (h, params) => {
            let ret = [];
            ret.push(
              h(
                'Button',
                {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.getTestJobDetail(params.row);
                    }
                  }
                },
                '查看详情'
              )
            );
            return h(
              'div',
              {
                style: {
                  align: 'center'
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
          width: '100px',
          fixed: 'right',
          render: (h, params) => {
            let ret = [];
            if (this.userInfo.identifyQA && this.userInfo.username === this.content.qa_username) {
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
                      this.setJobStatus(params.row);
                    }
                  }
                },
                '确认结果'
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
                  '确认结果'
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
  mounted: async function () {
    this.initData();
    await this.searchIcafeDetail();
    await this.CheckUserInfo();
    await this.getDetails();
  },
  computed: {
  },
  components: {
  },
  methods: {
    changeTimestamp(timestamp, offset = 8) {
      if (timestamp) {
        let date = timestampToTime(timestamp, offset);
        let dt = dateFmt(date, 'yyyy-MM-dd hh:mm:ss');
        return dt;
      } else {
        return '';
      }
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
    async searchIcafeDetail() {
      this.content = null;
      let params = {
        sequence: this.$route.params.reqid
      };
      const {code, data, message} = await api.get(AssociateBugUrl, params);
      if (parseInt(code, 10) === 200) {
        this.content = data[0];
        console.log('icafe detail is', this.content);
      } else {
        this.content = null;
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async CheckUserInfo() {
      const { code, data, message } = await api.get(UserCheckUrl);
      if (parseInt(code, 10) === 200) {
        this.userInfo.identifyQA = data.identifyQA;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getDetails() {
      this.datas = [];
      let params = {
        icafe_id: this.$route.params.reqid
      };
      const { code, data, message } = await api.get(RequriementDetailUrl, params);
      if (parseInt(code, 10) === 200) {
        // 塞到datas的detais 字段里面
        this.datas = data;
      } else {
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    jumper(url) {
      // 跳转到相应的需求页,自己的工作台 todo
      window.open(url, '_blank');
    },
    setJobStatus(row) {
      this.selectRow = row;
      this.showApproveModa = true;
    },
    async handleReset() {
      this.initData();
    },
    initData() {
      this.showApproveModa = false;
      this.approve = 'pass';
      this.selectRow = null;
    },
    async handleSubmit() {
      await this.TestJobDone();
      this.initData();
    },
    // 标记icafe测试完成
    async TestJobDone(row) {
      let params = {
        method: '确认',
        icafe_id: this.$route.params.reqid,
        rd: this.$route.query.rd,
        qa: this.$route.query.qa,
        test_id: this.selectRow.test_id,
        approve: this.approve
      };
      const { code, message } = await api.put(StartTestUrl, params);
      if (parseInt(code, 10) === 200) {
        await this.getDetails();
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getTestJobDetail(item) {
      // 获取最新一次任务的进度
      let _params = {
        jid: item.test_id
      };
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'SingleDetail', params: _params});
      window.open(href, '_blank');
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

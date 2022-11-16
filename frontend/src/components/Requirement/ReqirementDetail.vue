<template>
  <div>
   <Card
      class="center-card-s"
      v-if="datas.length > 0"
    >
      <div>
        <Row style="margin-top: 1%;">
          <Col>
            需求title: {{ $route.query.title }}
          </Col>
          <Col offset="1">
            RD: {{ $route.query.rd }}
          </Col>
          <Col offset="1">
            QA: {{ $route.query.qa }}
          </Col>
          <Col offset="1">
          Repo: {{ $route.query.repo }}
          </Col>
          <Col offset="1">
          pr: {{ $route.query.pr }}
          </Col>
        </Row>
      </div>
    </Card>
   <Card
      class="center-card-s"
      v-if="datas.length > 0"
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
  </div>
</template>

<script>
import { RequriementDetailUrl } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'ReqDetails',
  props: {},
  data: function () {
    return {
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
          align: 'center'
        },
        {
          title: '详细结果',
          key: 'report',
          align: 'center',
          fixed: 'right',
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
        }
      ]
    };
  },
  mounted: async function () {
    await this.getDetails();
  },
  computed: {
  },
  components: {
  },
  methods: {
    getStatus(status) {
      console.log('status', status);
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
    jumper() {
      // 跳转到相应的需求页,自己的工作台 todo
      console.log('desc', this.req);
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

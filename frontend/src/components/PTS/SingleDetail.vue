<template>
  <div>
    <div class="center-card-s">
      <Row style="margin-top: 1%;">
        <span style="display:inline-block;width:95%;margin-right:2%;">
          <span> 环境配置: </span>
          <span> {{ getDisplay(env) }}</span>
        </span>
      </Row>
      <Row style="margin-top: 1%;" v-if="req">
        <span style="display:inline-block;width:95%;margin-right:2%;">
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
          :data="data"
          style="background-color:green;"
        ></Table>
      </Row>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SingleDetail',
  props: {},
  data: function () {
    return {
      req: {
        id: 3,
        desc: 'xxxx'
      },
      env: {},
      data: [],
      columns: [
        {
          title: '测试项',
          key: 'content',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
                style: {
                  marginRight: '5px',
                  color: this.setColor(params.row.status)
                }
              }, params.row.status)
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
                  color: 'blue'
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
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'info'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleDetail(params.row);
                  }
                }
              }, '查看')
            ]);
          }
        }
      ]
    };
  },
  mounted: function () {
    this.getData();
  },
  components: {
  },
  methods: {
    async getData() {
      let jid = this.$route.params.jid;
      let params = {
        jid: jid
      };
      this.env = {
        os: 'linux',
        python: 'python3.7',
        value: '23344',
        type: 'pr',
        branch: 'develop',
        cuda: 'cuda10.2'
      };
      this.data = [
        {
          content: 'API测试',
          status: 'error',
          result: {
            success: 10,
            error: 5,
            skip: 3
          },
          create_time: '2022-10-26 19:00:35'
        },
        {
          content: '动转静测试',
          status: 'success',
          result: {
            success: 10,
            error: 0,
            skip: 0
          },
          create_time: '2022-10-27 18:31:35'
        }
      ];
      console.log('search detail by jid', params);
    },
    initData() {
      this.env = {};
      this.data = [];
    },
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'done':
          return 'green';
        case 'success':
          return 'green';
        case 'passed':
          return 'green';
        case 'pass':
          return 'green';
        case 'warning':
          return 'yellow';
        case 'error':
          return 'red';
        case 'fail':
          return 'red';
        case 'failed':
          return 'red';
        default:
          return 'red';
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
      let sucess_num = row.result.success;
      let error_num = row.result.error;
      let skip_num = row.result.skip;
      let detail = `成功${sucess_num}个,失败${error_num}个,跳过${skip_num}`;
      return detail;
    },
    getDisplay(env) {
      let content_list = [];
      let key_list = ['os', 'branch', 'value', 'python', 'cuda'];
      for (let i = 0; i <= key_list.length; i++) {
        let key = key_list[i];
        if (env[key]) {
          if (key === 'value') {
            let con = env.type + ':' + env[key];
            content_list.push(con);
          } else if (key === 'branch') {
            if (env[key]) {
              content_list.push(env[key]);
            }
          } else {
            content_list.push(env[key]);
          }
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

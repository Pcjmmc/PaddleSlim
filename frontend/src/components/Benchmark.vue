<template>
  <div>
    <div style="margin-top: 1.5%">
      <Row
        type="flex"
        justify="start"
        class="all-line-row"
      >
        <Col span="3">
          <Input
            clearable
            v-model="jid"
            placeholder="输入job id"
          ></Input>
        </Col>
        <Col span="1" offset="1">
          <Button
            icon="ios-search"
            type="primary"
            @click="getData"
          >search</Button>
        </Col>
      </Row>
    </div>
    <div style="margin-top: 1.5%">
      <span style="text-align: center;font-size: 1.2em;"> job 信息 </span>
      <vue-json-pretty
        :data="job"
      >
      </vue-json-pretty>
    </div>
    <span style="text-align: center;font-size: 1.2em;"> case 详情 </span>
    <Table
      border
      :columns="columns11"
      :data="details"
    ></Table>
  </div>
</template>
<script>
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import api from '../api/index';
import { OpBenchmarkUrl } from '../api/url.js';

export default {
  data() {
    return {
      jid: null,
      details: [],
      job: {},
      ShowDetail: false,
      ErrorDetail: {},
      columns11: [
        {
          title: '配置',
          key: 'yaml',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Tooltip', {
                props: {
                  placement: 'right',
                  transfer: true
                }
              }, [params.row.yaml.value, h('vue-json-pretty', {
                slot: 'content',
                props: {
                  data: params.row.yaml.conf_detail
                }
              })
              ])
            ]);
          }
        },
        {
          title: 'API',
          key: 'paddle_api'
        },
        {
          title: 'CaseName',
          width: 120,
          key: 'case_name'
        },
        {
          title: '前向',
          align: 'center',
          children: [
            {
              title: 'paddle',
              key: 'paddle_forward',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.paddle_forward + 's')
                ]);
              }
            },
            {
              title: 'torch',
              key: 'torch_forward',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.torch_forward + 's')
                ]);
              }
            }
          ]
        },
        {
          title: '反向',
          align: 'center',
          children: [
            {
              title: 'paddle',
              key: 'paddle_backward',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.paddle_backward + 's')
                ]);
              }
            },
            {
              title: 'torch',
              key: 'torch_backward',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.torch_backward + 's')
                ]);
              }
            }
          ]
        },
        {
          title: '整体',
          align: 'center',
          children: [
            {
              title: 'paddle',
              key: 'paddle_total',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.paddle_total + 's')
                ]);
              }
            },
            {
              title: 'torch',
              key: 'torch_total',
              align: 'center',
              render: (h, params) => {
                return h('div', [
                  h('span', {
                  }, params.row.torch_total + 's')
                ]);
              }
            }
          ]
        },
        {
          title: '前向差距',
          key: 'compare_forward',
          align: 'center',
          render: (h, params) => {
            const { compare_forward } = params.row;
            return h('div', [
              h('span', {
                style: {
                  color: compare_forward < 0 ? 'red' : 'green'
                }
              }, compare_forward + 'x')
            ]);
          }
        },
        {
          title: '反向差距',
          key: 'compare_backward',
          align: 'center',
          render: (h, params) => {
            const { compare_backward } = params.row;
            return h('div', [
              h('span', {
                style: {
                  color: compare_backward < 0 ? 'red' : 'green'
                }
              }, compare_backward + 'x')
            ]);
          }
        },
        {
          title: '整体差距',
          key: 'compare_total',
          align: 'center',
          render: (h, params) => {
            const { compare_total } = params.row;
            return h('div', [
              h('span', {
                style: {
                  color: compare_total < 0 ? 'red' : 'green'
                }
              }, compare_total + 'x')
            ]);
          }
        }
      ]
    };
  },
  mounted() {
    this.getData();
  },
  components: {
    VueJsonPretty
  },
  methods: {
    async getData() {
      // 判断参数如果参数中有tag，则name=version；如果没有，则name=release+version
      let params = {
        jid: this.jid
      };
      const { code, data } = await api.get(OpBenchmarkUrl, params);
      if (parseInt(code, 10) === 200) {
        this.job = data.job;
        this.details = data.case_detail;
        // console.log(this.details);
      } else {
        this.details = [];
        this.$Message.error({
          content: '请求出错: ',
          duration: 30,
          closable: true
        });
      }
    }
  }
};
</script>

<style scoped>
.all-line-row {
  margin-bottom: 0.5%;
  margin-left: 0.5%;
}
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow:auto;
}
</style>

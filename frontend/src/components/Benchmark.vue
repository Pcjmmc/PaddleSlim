<template>
    <Table
     border
    :columns="columns11"
    :data="details"
  ></Table>
</template>
<script>
import api from '../api/index';
import { OpBenchmarkUrl } from '../api/url.js';

export default {
  data() {
    return {
      details: [],
      columns11: [
        {
          title: '配置',
          key: 'yaml',
          align: 'center'
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
              align: 'center'
            },
            {
              title: 'torch',
              key: 'torch_forward',
              align: 'center'
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
              align: 'center'
            },
            {
              title: 'torch',
              key: 'torch_backward',
              align: 'center'
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
              align: 'center'
            },
            {
              title: 'torch',
              key: 'torch_total',
              align: 'center'
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
              }, compare_forward)
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
              }, compare_backward)
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
              }, compare_total)
            ]);
          }
        }
      ]
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      // 判断参数如果参数中有tag，则name=version；如果没有，则name=release+version
      const { code, data } = await api.get(OpBenchmarkUrl);
      if (parseInt(code, 10) === 200) {
        this.details = data;
        console.log(this.details);
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

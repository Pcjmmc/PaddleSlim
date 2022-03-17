<template>
  <div>
    <row style="margin-bottom: 20px;">
      <col>
        <h3> {{ query_params.tname }} </h3>
        <div v-if="query_params.status=='pass'" style="margin-left: 10px;">
          <Button type="success" shape="circle" size="small" >success</Button>
        </div>
        <div v-else style="margin-left: 10px;">
          <Button type="error" shape="circle" size="small" >fail</Button>
        </div>
      </col> 
    </row>
    <row>
      <col style="margin-left: 30px;">
        <ApiCoverage :percent="80" :total="2000" description="覆盖case数" content="任务Api覆盖程度"> </ApiCoverage>
      </col>
      <col slot="right">
        <ApiDistribution> </ApiDistribution>
      </col>
    </row>
    <row style="margin-bottom: 10px;">
      <Table
        :columns="envColumn"
        :data="params"
        style="margin-right: 2%;width: 98%;"
      >
      </Table>
    </row>
  </div>
</template>

<script>
import ApiCoverage from './ApiCoverage.vue';
import ApiDistribution from './ApiDistribution.vue';
import TableBase from './TableBase.vue'
export default {
  name: 'ApiDetails',
  props: {},
  data: function () {
    return {
      query_params: [],
      params: [],
      envColumn: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            return h(TableBase, {
                props: {
                    params: params.row.data
                }
            });
          }
        },
        {
          title: 'api',
          key: 'name',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            const { status } = params.row;
            return h('div', [
                h('Tag', {
                props: {
                    color: ['pass', 'success'].indexOf(status.toLowerCase()) >= 0 ? 'green' : 'red'
                }
                }, status)
            ]);
          }
        },
        {
          title: 'op列表',
          key: 'oplist',
          align: 'center',
          render: (h, params) => {
          const { oplist } = params.row;
            return h('div', [
                h('Tooltip', {
                }, oplist ? oplist[0] : '')
            ]);
          }
        },
        {
          title: '标签列表',
          key: 'tags',
          align: 'center',
          render: (h, params) => {
          const { tags } = params.row;
            return h('div', [
                h('Tooltip', {
                }, tags ? tags[0] : '')
            ]);
          }
        }
      ]
    };
  },
  mounted: function () {
    this.query_params = this.$route.query;
    this.getData();
  },
  components: {
    ApiCoverage,
    ApiDistribution
  },
  methods: {
    async getData() {
      this.initData();
      this.params = [
        {
         'name': 'test_api',
         'status': 'pass',
         'data': [
            {
              'name': '静态图',
              'forward': true,
              'backward': true,
              'performance': false,
              'accurate': true,
              'exception': true
            },
            {
             'name': '动态图',
             'forward': true,
              'backward': true,
              'performance': false,
              'accurate': true,
              'exception': true
            }
          ],
         'tags': ['dy_to_static'],
         'oplist': []
        },
        {
         'name': 'add_elements',
         'status': 'pass',
         'tags': ['dy_to_static'],
         'oplist': ['_add', '_init'],
         'data': [
            {
              'name': '静态图',
              'forward': true,
              'backward': true,
              'performance': false
            },
            {
             'name': '动态图',
             'forward': true,
              'backward': true,
              'performance': false,
              'accurate': false,
              'exception': false
            }
          ]
        }
      ]
    },
    initData() {
      this.params = [];
    }
  }
};
</script>
<style scoped>
</style>
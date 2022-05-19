<template>
  <div
    style="margin-bottom: 10px;"
  >
    <Table
        size="small"
        :columns="Columns"
        :data="kpis"
        style="margin-right: 2%"
    >
    </Table>
  </div>
</template>

<script>

export default {
  name: 'DetailBase',
  props: {
    'kpis': {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      Columns: [
        {
          title: '指标名',
          key: 'kpi_name',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
              }, this.caculateKpiName(params.row))
            ]);
          }
        },
        {
          title: '状态',
          key: 'kpi_status',
          align: 'center'
        },
        {
          title: '基准值',
          key: 'kpi_base',
          align: 'center'
        },
        {
          title: '当前值',
          key: 'kpi_value',
          align: 'center',
          render: (h, params) => {
            // console.log('params.row', params.row);
            const { kpi_status, kpi_value } = params.row;
            return h('div', [
              h('Tag', {
                props: {
                  color: kpi_status.toLowerCase() === 'passed' ? 'success' : 'error'
                }
              }, kpi_value)
            ]);
          }
        },
        {
          title: '阈值',
          key: 'threshold',
          align: 'center'
        },
        {
          title: '比率',
          key: 'ratio',
          align: 'center',
          render: (h, params) => {
            const { threshold, ratio } = params.row;
            return h('div', [
              h('Tag', {
                props: {
                  color: Math.abs(ratio) > threshold ? 'red' : 'green'
                }
              }, ratio)
            ]);
          }
        },
        {
          title: '变化趋势',
          key: 'trend',
          align: 'center'
        }
        // {
        //   title: 'case日志',
        //   key: 'log',
        //   align: 'center',
        //   minWidth: 200,
        //   render: (h, params) => {
        //     // console.log('baseulr', this.baseulr);
        //     return h('div', [
        //       h('a', {
        //         attrs: {
        //           href: this.getCaseLogUrl(params.row.log_path)
        //         }
        //       }, this.getCaseLogUrl(params.row.log_path))
        //     ]);
        //   }
        // }
      ]
    };
  },
  mounted: function () {
    // console.log('this params', this.model_name, this.kpis);
  },
  components: {
  },
  methods: {
    caculateKpiName(row) {
      let name = [];
      if (row.step_name) {
        name.push(row.step_name);
      }
      if (row.tag) {
        name.push(row.tag);
      }
      name.push(row.kpi_name);
      return name.join('_');
    }
  }
};
</script>


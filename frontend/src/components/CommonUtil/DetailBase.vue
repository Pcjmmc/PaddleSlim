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
    },
    'failState': {
      type: [Object],
      default: function () {
        return {};
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
          align: 'center',
          minWidth: 120,
          render: (h, params) => {
            const { kpi_status } = params.row;
            let ret = [];
            ret.push(
              h('Tag', {
                props: {
                  color: kpi_status.toLowerCase() === 'passed' ? 'success' : 'error'
                }
              }, kpi_status)
            );
            if (kpi_status.toLowerCase() === 'failed') {
              ret.push(
                h('Button', {
                props: {
                  size: 'small',
                  type: 'primary'
                },
                on: {
                  click: () => {
                    this.autoBinarySearch(params.row);
                  }
                }
              }, '自动定位'));
              if (this.dealWithTag(params.row) in this.failState) {
                ret.push(
                h('div', {
                }, [
                  h('p', {
                    style: {
                      display: 'inline-block'
                    }
                  }, '任务链接：'),
                  h('a', {
                    style: {
                      dispaly: 'block'
                    },
                    attrs: {
                      href: this.getXlyLink(params.row),
                      target: '_blank'
                    }
                  }, '点击跳转'),
                  h('p', {
                  style: {
                    display: 'block'
                  }
                }, '当前状态: ' + this.getStatus(params.row))
                ])
               );
              }
            }
            return h(
              'div',
              {
                style: {
                  display: 'block',
                  flexWrap: 'wrap',
                  justifyContent: 'center',
                  alignItems: 'center'
                }
              },
              ret
            );
          }
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
          minWidth: 120,
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
    // console.log('failState', this.failState);
  },
  components: {
  },
  inject: ['fatherMethod'],
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
    },
    dealWithTag(row) {
      return row.tag.split('_')[1];
    },
    autoBinarySearch(row) {
      let tag =  this.dealWithTag(row);
      let params = {
        model_name: row.model_name,
        tag_name: tag,
        step_name: row.step_name
      };
      // console.log(params);
      this.fatherMethod(params);
    },
    getXlyLink(row) {
      let tag =  this.dealWithTag(row);
      let innerValue = this.failState[tag];
      if (innerValue) {
        return innerValue.xly_link;
      } else {
        return '';
      }
    },
    getStatus(row) {
      let tag =  this.dealWithTag(row);
      if (tag in this.failState) {
        let status = this.failState[tag].status;
        // console.log(status);
        switch (status) {
          case 'quening':
            return '排队中';
          case 'preparing':
            return '测试准备';
          case 'release':
            return '框架release测试';
          case 'locationing':
            return '定位问题PR';
          case 'finished':
            return '定位结束';
          case 'canceled':
            return '任务取消';
          case 'failed':
            return '任务失败';
          default:
            // console.log(this.statusStored[row.step_name]);
            return '任务过期请重新定位';
        }
      }
    }
  }
};
</script>


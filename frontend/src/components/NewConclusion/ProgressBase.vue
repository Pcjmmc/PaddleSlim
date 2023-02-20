<template>
  <div style="margin-left: 1%;">
    <div>
      <Table :columns="columns7" :data="datas"></Table>
    </div>
  </div>
</template>

<script>

export default {
  name: 'SummaryBase',
  props: {
    datas: {
      type: [Array],
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
      columns7: [
        {
          title: '阶段',
          align: 'center',
          key: 'step',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.step)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.step)
              ]);
            }
          }
        },
        {
          title: '总量',
          align: 'center',
          key: 'total',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.total)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.total)
              ]);
            }
          }
        },
        {
          title: '成功',
          align: 'center',
          key: 'pass',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.pass)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.pass)
              ]);
            }
          }
        },
        {
          title: '失败',
          align: 'center',
          key: 'fail',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold',
                    color: 'red'
                  }
                }, params.row.fail)
              ]);
            } else {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold',
                    color: 'red'
                  }
                }, params.row.fail)
              ]);
            }
          }
        },
        {
          title: '运行中',
          align: 'center',
          key: 'running',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.running)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.running)
              ]);
            }
          }
        },
        {
          title: '轮数',
          align: 'center',
          key: 'round',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.round)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.round)
              ]);
            }
          }
        },
        {
          title: '进度',
          align: 'center',
          key: 'progress',
          render: (h, params) => {
            if (params.index === 0) {
              return h('div', [
                h('span', {
                  style: {
                    fontWeight: 'bold'
                  }
                }, params.row.progress)
              ]);
            } else {
              return h('div', [
                h('span', {
                }, params.row.progress)
              ]);
            }
          }
        }
      ]
    };
  },
  watch: {
  },
  mounted: function () {
  },
  components: {
  },
  methods: {
  }
};
</script>

<style scoped>
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow: auto;
  margin-bottom: 1%
}
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.ivu-form-item{
  margin-bottom: 12px;
  font-size: 14px;
}
</style>

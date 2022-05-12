<template>
    <div style="margin-bottom: 10px;">
      <Table
        :columns="columns"
        :data="params"
        style="width: 100%;"
      >
      </Table>
    </div>
</template>

<script>
export default {
  name: 'TableBase',
  props: {
    'params': {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      columns: [
        {
          title: '动或静',
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
                    color: ['passed', 'pass', 'success'].indexOf(status.toLowerCase()) >= 0 ? 'success' : 'error'
                }
                }, status)
            ]);
          }
        },
        {
          title: '前向',
          key: 'forward',
          align: 'center',
          render: (h, params) => {
            const { forward } = params.row;
            if (forward) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        },
        {
          title: '反向',
          key: 'backward',
          align: 'center',
          render: (h, params) => {
            const { backward } = params.row;
            if (backward) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        },
        {
          title: '参数',
          key: 'parameters',
          align: 'center',
          render: (h, params) => {
            const { parameters } = params.row;
            if (parameters) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        },
        {
          title: '精度',
          key: 'accurate',
          align: 'center',
          render: (h, params) => {
            const { accurate } = params.row;
            if (accurate) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        },
        {
          title: '性能',
          key: 'performance',
          align: 'center',
          render: (h, params) => {
            const { performance } = params.row;
            if (performance) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        },
        {
          title: '异常',
          key: 'exception',
          align: 'center',
          render: (h, params) => {
            const { exception } = params.row;
            if (exception) {
              return h('Icon', {
                props: {
                  type: 'ios-checkmark',
                  color: 'green'
                }
              })
            } else {
              return h('span', '-')
            }
          }
        }
      ]
    };
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
</style>
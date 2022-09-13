<template>
  <div>
    <Table
      border
      :columns="columns"
      :data="datas"
      style="width: 100%;margin-top: 1%;"
      >
      </Table>
  </div>
</template>

<script>

import { isEmpty } from '../../util/help.js';

export default {
  name: 'icafeBase',
  props: {
    datas: {
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
          title: '标题',
          key: 'title',
          align: 'center',
          fixed: 'left'
        },
        {
          title: '等级',
          key: 'level',
          align: 'center'
        },
        {
          title: 'rd负责人',
          key: 'rd_owner',
          align: 'center'
        },
        {
          title: 'qa负责人',
          key: 'qa_owner',
          align: 'center'
        },
        {
          title: '创建日期',
          key: 'createdTime',
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
                style: {
                  'font-size': '14px'
                },
                props: {
                  color: this.setColor(status)
                }
                }, status)
            ]);
          }
        },
        {
          title: '卡片详情',
          key: 'url',
          fixed: 'right',
          render: (h, params) => {
            return h('div', [h('a', {
              attrs: {
                href: params.row.url
              }
            }, isEmpty(params.row.url) === false ? '详情' : '-')]);
          }
        }
      ]
    };
  },
  mounted: function () {
  },
  components: {
  },
  computed: {
  },
  methods: {
    setColor(status) {
      switch (status) {
        case '已关闭':
          return 'success';
        case '开发中':
          return 'primary';
        case '测试中':
          return 'waring';
        case '测试完成':
          return 'success';
        default:
          return 'error';
      }
    }
  }
};
</script>

<style scoped>

</style>
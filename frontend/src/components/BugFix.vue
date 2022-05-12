<template>
<div>
    <row type="flex" justify="center" align="middle">
      <histogram-base
      ref="child"
      :xdata="newfilterst"
      :count="count"
    > </histogram-base>
    </Row>
    <div>
      <Divider orientation="left" style="font-size: 0.5em;font-style: italic;">bug列表</Divider>
    </div>
    <div style="margin-bottom: 10px;">
      <Table
        :columns="columns"
        :data="datas"
        style="width: 100%;"
      >
      </Table>
    </div>
  </div>
</template>
<script>
import HistogramBase from './HistogramBase.vue';
import { isEmpty } from "../util/help.js";
export default {
  name: 'BugFix',
  props: {
    datas: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  data: function () {
    return {
      count: [],
      newfilterst: [],
      columns: [
        {
          title: '标题',
          key: 'title',
          align: 'center',
          width: '350'
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
          align: 'center',
          width: '150'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          filters: [
          ],
          filterMultiple: false,
          filterMethod (value, row) {
            return row.status == value;
          },
          render: (h, params) => {
            const { status } = params.row;
            return h('div', [
                h('Tag', {
                props: {
                    color: this.setColor(status)
                }
                }, status)
            ]);
          }
        },
        {
          title: '详情',
          key: 'url',
          render: (h, params) => {
            return h('div', [h('a', {
              attrs: {
                href: params.row.url
              }
            }, isEmpty(params.row.url) == false ? '详情' : '-')])
          }
        }
      ]
    }
  },
  components: {
    HistogramBase
  },
  watch: {
    datas: function () {
      this.getStatusFilters();
    }
  },
  mounted: function () {
    this.getStatusFilters();
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
        default:
          return 'error';
      }
    },
    getStatusFilters() {
      let filterst = [];
      let filters = [];
      let res = {};
      for (var i = 0; i < this.datas.length; i++) {
        let status = this.datas[i].status;
        filterst.push(status);
        if (!res[status]) {
          res[status] = 0;
        }
        res[status] += 1;
      }
      this.newfilterst = Array.from(new Set(filterst));
      for (var j = 0; j < this.newfilterst.length; j++) {
        this.count.push(res[this.newfilterst[j]]);
        filters[j] = {
          label: this.newfilterst[j],
          value: this.newfilterst[j]
        };
      }
      this.columns[5].filters = filters;
      this.$nextTick(function () {
        this.$refs.child.drawPie('main1');
      });
    }
  }
};
</script>

<style scoped>
.video-header {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
.container-content {
  overflow-y: auto;
}
</style>

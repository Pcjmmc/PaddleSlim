<template>
  <div>
    <!--
    <div>
      <row>
        <col style="margin-left: 30px;">
          <pie-base
            ref="cdpie"
            :column="sts_column"
            :xdata="sts_datas"
            v-if="sts_datas.length > 0"
          ></pie-base>
        </col>
        <col slot="right">
          <histogram-base
            ref="child"
            :xdata="dis_datas"
            :count="dis_count"
            v-if="dis_datas.length > 0"
          ></histogram-base>
        </col>
      </row>
    </div>
    -->
    <div>
      <!--
      <Divider orientation="left" style="font-size: 0.5em;font-style: italic;">bug列表</Divider>
      -->
      <h3>集测bug列表</h3>
    </div>
    <div>
      <Table
        :columns="columns"
        :data="datas"
        style="width: 100%;margin-top: 1%;"
      >
      </Table>
    </div>
    <!--
    <div style="margin-bottom: 10px;margin-top:2%;">
      <el-tabs
        type="card"
        v-model="childname"
        style="margin-left: 1%;"
        @tab-click="clickChildTab"
      >
        <el-tab-pane
        :label="item.desc"
        :key="index"
        :name="item.key"
        v-for="(item, index) in tasktypelist"
        >
          <Table
            :columns="columns"
            :data="datas"
            style="width: 100%;"
          >
          </Table>
        </el-tab-pane>
      </el-tabs>
    </div>
    -->
  </div>
</template>
<script>

import PieBase from './PieBase.vue';
import api from '../api/index';
import HistogramBase from './HistogramBase.vue';
import { isEmpty } from "../util/help.js";
import { BugUrl } from '../api/url.js';

export default {
  name: 'BugFix',
  props: {
    tasktypelist: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    tag: {
      type: [String],
      default: ''
    }
  },
  data: function () {
    return {
      // childname: 'compile',
      datas: [],
      dis_datas: [],
      dis_count: [],
      sts_datas: [],
      sts_column: [],
      columns: [
        {
          title: '标题',
          key: 'title',
          align: 'center',
          fixed: 'left'
        },
        {
          title: 'bug所属方向',
          key: 'task_type',
          align: 'center'
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
          title: '关联任务',
          key: 'log_url',
          render: (h, params) => {
            let arr = params.row.log_url;
            var newArr = [];
              arr.forEach((obj, index) => {
                newArr.push(h('div', [
                  h('a', {
                    props: {
                      href: 'javascript:void(0)'
                    },
                    style: {
                      'font-size': '8px',
                      size: 'small',
                      'margin-top': '5px'
                    },
                    on: {
                        click: () => {
                          this.openNew(obj.url);
                        }
                      }
                    }, obj.secondary_type)
                  ])
                );
              });
            return h('div', newArr);
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
            }, isEmpty(params.row.url) == false ? '详情' : '-')])
          }
        }
      ]
    }
  },
  components: {
    HistogramBase,
    PieBase
  },
  watch: {
    datas: function () {
      this.getStatusFilters();
    },
    tag: function () {
      this.getbugdata();
    }
  },
  mounted: function () {
    this.getbugdata();
    this.getStatusFilters();
  },
  methods: {
    openNew(url) {
      window.open(url, '_blank');
    },
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
    clickChildTab(item) {
      this.childname = item.name;
      this.datas = [];
      // 将选中的tab标记成蓝色
      // console.log('this child name', this.childname);
      this.getFilterData();
    },
    async getFilterData() {
      let _params = {'tag': this.tag, 'task_type': this.childname};
      const {code, data, version} = await api.get(BugUrl, _params);
      if (parseInt(code, 10) === 200) {
        this.datas = data;
      } else {
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + version,
          duration: 30,
          closable: true
        });
      }
    },
    async getbugdata() {
      let _params = {'tag': this.tag};
      const {code, data, version} = await api.get(BugUrl, _params);
      if (parseInt(code, 10) === 200) {
        this.datas = data;
        // this.dis_datas = data.dis_datas;
        // this.dis_count = data.dis_count;
        // this.sts_datas = data.sts_datas;
        // this.sts_column = data.sts_column;
        this.getStatusFilters();
      } else {
        // this.dis_datas = [];
        // this.dis_count = [];
        // this.sts_datas = [];
        // this.sts_column = [];
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + version,
          duration: 30,
          closable: true
        });
      }
    },
    getStatusFilters() {
      let filterst = [];
      let filters = [];
      for (var i = 0; i < this.datas.length; i++) {
        let status = this.datas[i].status;
        if (status) {
          filterst.push(status);
        }
      }
      this.newfilterst = Array.from(new Set(filterst));
      for (var j = 0; j < this.newfilterst.length; j++) {
        filters[j] = {
          label: this.newfilterst[j],
          value: this.newfilterst[j]
        };
      }
      this.columns[6].filters = filters;
      this.$nextTick(function () {
        if (this.sts_datas.length > 0) {
          this.$refs.cdpie.drawPieChart('chartPie');
        }
        if (this.dis_datas.length > 0) {
          this.$refs.child.drawPie('main1');
        }
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

<template>
<div>
    <row type="flex" justify="center" align="middle">
      <histogram-base> </histogram-base>
    </Row>
    <div>
      <Divider orientation="left" style="font-size: 0.5em;font-style: italic;">bug列表</Divider>
    </div>
    <div style="margin-bottom: 10px;">
      <Table
        :columns="columns"
        :data="bugList"
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
  props: ["data", "scenes"],
  data: function () {
    return {
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
          title: '负责人',
          key: 'rd_owner',
          align: 'center'
        },
        {
          title: 'QA',
          key: 'qa_owner',
          align: 'center'
        },
        {
          title: '创建日期',
          key: 'create_time',
          align: 'center',
          width: '150'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          filters: [
            {
              label: '开发中',
              value: '开发中'
            },
            {
              label: '新建',
              value: '新建'
            },
            {
              label: '测试中',
              value: '测试中'
            },
            {
              label: '测试完成',
              value: '测试完成'
            }
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
      ],
      bugList: []
    }
  },
  components: {
    HistogramBase
  },
  mounted: function () {
    this.getData();
  },
  methods: {
    setColor(status) {
      switch (status) {
        case '已关闭':
          return 'green';
        case '开发中':
          return 'blue';
        case '测试中':
          return 'yellow';
        default:
          return 'red';
      }
    },
    async getData(commit, branch) {
      // 参数主要是从icafe卡片筛选出相应的卡片，具体还是需要再定
      this.bugList = [
        {
          'title': '【Paddle Inference】win cuda11.0下单测失败', // 标题
          'level': 'P1',
          'rd_owner': '宝阿春',
          'qa_owner': '王也',
          'create_time': '2022-02-22 10:05',
          'url': 'https://console.cloud.baidu-int.com/devops/icafe/issue/DLTP-45162/show',
          'status': '新建'
        },
        {
          'title': '【Paddle Inference】win cuda11.0下单测失败', // 标题
          'level': 'P3',
          'rd_owner': '张留杰',
          'qa_owner': '罗泽宇',
          'create_time': '2022-02-14 18:46',
          'url': 'https://console.cloud.baidu-int.com/devops/icafe/issue/DLTP-43997/show',
          'status': '开发中'
        },
        {
          'title': 'pr:39573 导致PaddleNLP faster_ernie 模型python 预测报错', // 标题
          'level': 'P1',
          'rd_owner': '张云飞',
          'qa_owner': '刘换岭',
          'create_time': '2022-02-21 17:10',
          'url': 'https://console.cloud.baidu-int.com/devops/icafe/issue/DLTP-44863/show',
          'status': '已关闭'
        }
      ]
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

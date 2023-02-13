<template>
  <div>
    <Table :columns="columns7" :data="datas"></Table>
  </div>
</template>

<script>

import BaseResult from './BaseResult.vue';
import api from '../../api/index';
import { AssociateBugUrl } from '../../api/url.js';

export default {
  props: {
    idx: {
      type: [Number],
      default: function () {
        return 0;
      }
    },
    datas: {
      type: [Array],
      default: function () {
        return [];
      }
    }
  },
  data: function () {
    return {
      columns7: [
        {
          title: '标题',
          align: 'center',
          key: 'title',
          render: (h, params) => {
            let ret = []
            if (params.row.title) {
              ret.push(
                h('div', [h('a', {
                attrs: {
                  href: 'javascript:void(0)'
                },
                on: {
                  click: () => {
                    this.jumper(params.row.url);
                  }
                }
              }, params.row.title)]))
            } else {
              ret.push(
                h("Input", {
                  props: {
                    value: params.row.url,
                    placeholder: '请输入卡片序列号!'
                  },
                  on: {
                    input: val => {
                      params.row.url = val;
                      // 发送请求，获取相关信息
                    },
                    'on-blur': async () => {
                      await this.getIcafeInfo(params.index, params.row);
                    }
                  }
                })
              )
            }
            return h(
              'div',
              ret
            )
          }
        },
        {
          title: '负责人',
          align: 'center',
          key: 'owner'
        },
        {
          title: '操作',
          align: 'center',
          key: 'operation',
          render: (h, params) => {
            let ret = []
            ret.push(
              h(
                'Button',
                {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.deleteIcafeItem(params.index, params.row);
                    }
                  }
                },
                '删除'
              )
            )
            return h(
              'div',
              ret
            )
          }
        }
      ]
    };
  },
  watch: {
  },
  components: {
  },
  mounted: async function () {
  },
  computed: {
  },
  methods: {
    jumper(url) {
      // 根据branch获取commit列表
      window.open(url, '_blank');
    },
    deleteIcafeItem(index) {
      // 赋值成当前选择的icafe todo
      if (this.datas.length < 1) {
        return false;
      }
      this.datas.splice(index, 1);
    },
    async getIcafeInfo(index, row) {
      // 发送icafe请求
      let params = {
        sequence: row.url
      };
      const {code, data, message} = await api.get(AssociateBugUrl, params);
      if (parseInt(code, 10) === 200 && data.length > 0) {
        let info = data[0];
        this.datas[index].title = info.title;
        this.datas[index].owner = info.rd_owner;
        this.datas[index].url = info.url;
        this.$emit('updataDate', this.idx, this.datas);
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    }
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
</style>

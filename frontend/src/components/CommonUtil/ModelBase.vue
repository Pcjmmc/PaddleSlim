<template>
    <div
        style="margin-bottom: 10px;"
    >
        <Tag style="font-size:15px">模型名: {{ modelName }} </Tag>
        <Tag
          v-if="status.toLowerCase()=='passed'"
          style="font-size:15px"
          color="success"
        >模型状态: {{ status }} </Tag>
        <Tag
          style="font-size:15px"
          color="error"
          v-else
        >模型状态: {{ status }} </Tag>
        <Table
          border
          size="small"
          :columns="Columns"
          :data="kpis"
          style="margin-right: 2%;"
        >
        </Table>
      <Modal
        width="700px"
        v-model="show"
        title="任务链接"
        v-on:on-cancel="handleClose"
      >
        <div>
          <a
            href="javascript:void(0)"
            style="font-size:14px;margin-left:2%;"
            @click="jumper(joburl)"
          > {{ joburl }} </a>
        </div>
        <div slot="footer">
          <Button type="primary" @click="handleClose">确定</Button>
        </div>
      </Modal>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
import DetailBase from './DetailBase.vue';
import { AutoBinarySearchUrl } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'ModelBase',
  props: {
    'modelName': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'kpis': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    'status': {
      type: [String],
      default: function () {
        return '';
      }
    }
  },
  data: function () {
    return {
      joburl: '',
      show: false,
      Columns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            // console.log('params', this.modelName);
            return h(DetailBase, {
                props: {
                    kpis: params.row.data
                }
            });
          }
        },
        {
          title: '阶段名',
          key: 'step_name',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            let ret = [];
            if (params.row.status) {
              ret.push(
                h('Tag', {
              }, params.row.status));
            }
            if (params.row.status.toLowerCase() === 'failed') {
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
            } else {
              // zhanwei
              ret.push(
                h('Button', {
                style: {
                  visibility: 'hidden'
                },
                props: {
                  disabled: true,
                  size: 'small',
                  type: 'primary'
                },
                on: {
                  click: () => {
                    this.jumper(params.row);
                  }
                }
              }, '自动定位'));
            }
            return h(
              'div',
              {
                style: {
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'center',
                  alignItems: 'center'
                }
              },
              ret
            );
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
    async autoBinarySearch(row) {
      let params = {
        repo_name: this.$route.query.reponame,
        model_name: this.modelName,
        step_name: row.step_name,
        email_add: Cookies.get('username') + '@baidu.com'
      };
      const {code, data, message} = await api.post(AutoBinarySearchUrl, params);
      if (parseInt(code, 10) === 200) {
        this.joburl = data.url;
        this.show = true;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    handleClose() {
      this.joburl = '';
      this.show = false;
    },
    jumper(url) {
      window.open(url, '_blank');
    }
  }
};
</script>
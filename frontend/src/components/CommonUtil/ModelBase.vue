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
    </div>
</template>

<script>
import Cookies from 'js-cookie';
import DetailBase from './DetailBase.vue';
import { AutoBinarySearchUrl, PublishBinary } from '../../api/url.js';
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
  provide() {
    return {
      fatherMethod: this.autoBinarySearch
    };
  },
  data: function () {
    return {
      statusStored: {},
      Columns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            if (params.row.status.toLowerCase() === 'failed' && params.row.step_name in this.statusStored) {
              return h(DetailBase, {
                props: {
                    kpis: params.row.data,
                    failState: this.statusStored[params.row.step_name]
                }
              });
            } else {
              return h(DetailBase, {
                props: {
                    kpis: params.row.data
                }
              });
            }
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
                  props: {
                  color: params.row.status.toLowerCase() === 'passed' ? 'success' : 'error'
                }
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
              if (this.isInDate(params.row)) {
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
                      href: this.getUrl(params.row),
                      target: '_blank'
                    }
                  }, this.getUrl(params.row)),
                  h('p', {
                  style: {
                    display: 'block'
                  }
                }, '当前状态: ' + this.getStatus(params.row))
                ])
              );
              }
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
                  display: 'block',
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
    this.updateStatus();
  },
  components: {
  },
  methods: {
    async autoBinarySearch(row) {
      // console.log('autoBinarySearch', row);
      let params = {
        repo_name: this.$route.query.reponame,
        model_name: row.model_name ? row.model_name : this.modelName,
        step_name: row.step_name,
        tag: 'tag_name' in row ? row.tag_name : 'default',
        email_add: Cookies.get('username') + '@baidu.com'
      };
      const {code, data, message} = await api.post(AutoBinarySearchUrl, params);
      // console.log(data);
      if (parseInt(code, 10) === 200) {
        let res = {};
        res.xly_link = data.url;
        res.status = data.status;
        this.updateStatus();
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
    },
    async updateStatus() {
      if (this.status !== 'Failed') {
        return;
      }
      let params = {
        email: Cookies.get('username') + '@baidu.com',
        repo_name: this.$route.query.reponame,
        model_name: this.modelName
      };
      const {code, data, message} = await api.get(PublishBinary, params);
      if (parseInt(code, 10) === 200) {
        this.statusStored = data;
        // console.log(this.statusStored);
      } else {
        this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
          });
      }
    },
    isInDate(row) {
      if (row.step_name in this.statusStored) {
        let step =  this.statusStored[row.step_name];
        if (step.default) {
          return true;
        }
      }
      return false;
    },
    getUrl(row) {
      return this.statusStored[row.step_name].default.xly_link;
    },
    getStatus(row) {
      if (row.step_name in this.statusStored) {
        let status = this.statusStored[row.step_name].default.status;
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
            return '未知状态';
        }
      }
    },
    getStatuses(step_name) {
      return this.statusStored.step_name;
    }
  }
};
</script>
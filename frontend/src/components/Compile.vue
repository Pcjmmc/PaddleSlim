<template>
  <div>
    <Card class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
          <Icon type="ios-information-circle" size="20"></Icon>
          {{ "任务信息概述" }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em; margin-top: 5%">
        任务名: {{ $route.query.tname }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: green"
        v-else
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        原因: {{ getErrorReason($route.query.exit_code) }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        repo信息: {{ $route.query.repo }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        commit信息: {{ $route.query.commit_id }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        分支信息: {{ $route.query.branch }}
      </p>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(env_info) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-document" size="20"></Icon>
        {{ "编译环境" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="env_info"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(compile_param) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-bookmarks" size="20"></Icon>
        {{ "编译参数" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="compile_param"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(gpu_arch) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-cloud-download" size="20"></Icon>
        {{ "产物详情" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="gpu_arch"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
  </div>
</template>

<script>
import Clipboard from 'clipboard';
import api from '../api/index';
import { DetailUrl } from '../api/url.js';
export default {
  data: function () {
    return {
      detail: {},
      column: [
        {
          title: '选项',
          key: 'key'
        },
        {
          title: '取值',
          key: 'value',
          render: (h, params) => {
            var key = params.row.key;
            var value = params.row.value;
            let arr = []
            var newArr = [];
            if (key == 'artifact_url') {
              if (value instanceof Array) {
                arr = value;
              } else {
                arr = [value];
              }
              arr.forEach((url, index) => {
                newArr.push(h('div', [
                  h('a', {
                    }, url),
                    h('Poptip', {
                      props: {
                        trigger: 'hover',
                        placement: 'top',
                        // 注意一定要添加该属性，否则表格会遮盖住气泡浮框
                        transfer: true,
                        content: '复制'
                      }
                    },
                    [
                      h('Icon', {
                        class: 'ivu-icon ivu-icon-ios-copy-outline copyBtn',
                        props: {
                            type: 'ios-copy-outline',
                            size: '20',
                            color: 'green'
                        },
                        on: {
                          click: () => {
                            let clipboard = new Clipboard('.copyBtn', {
                                text: function (trigger) {
                                  clipboard.destroy();
                                  return url;
                                }
                            });
                            clipboard.on('success', e => {
                              this.$Message.success('复制成功~');
                              e.clearSelection();
                            });
                            clipboard.on('error', e => {
                              this.$Message.error('复制失败,请手动复制~');
                            });
                          }
                        }
                      })
                    ])
                  ])
                );
              });
            } else {
              newArr.push(
                h('div', [h('span', {}, value)
                ])
              );
            }
            return h('div', newArr);
          }
        }
      ],
      env_info: [],
      compile_param: [],
      gpu_arch: []
    };
  },
  mounted: function () {
    this.getData();
  },
  components: {
  },
  computed: {
  },
  methods: {
    getErrorReason(exit_code) {
      switch (parseInt(exit_code, 10)) {
        case 0:
          return '成功';
        case 2:
          return 'CE框架失败';
        case 3:
          return '模型yaml书写错误';
        case 4:
          return 'Lite模型优化失败';
        case 5:
          return '未录入任务';
        case 7:
          return '编译失败';
        case 8:
          return 'case失败';
        case 63:
          return '克隆代码失败';
        case 125:
          return '启动容器失败';
        case 127:
          return 'tc没有执行权限';
        case 137:
          return 'tc任务取消';
        default:
          return '未知';
      }
    },
    getColumn(obj) {
      let _columns = []
      if (obj.length > 0) {
        let tmpobj = obj[0];
        for (let key in tmpobj) {
          _columns.push(key);
        }
      }
      let result = [];
      for (let idx = 0; idx < _columns.length; idx++) {
        let tmp = {
          title: _columns[idx],
          key: _columns[idx]
        };
        result.push(tmp)
      }
      console.log(result)
      return result
    },
    pocessData(obj) {
      let result = [];
      for (let key in obj) {
        let tmp = {
          key: key,
          value: obj[key]
        };
        result.push(tmp)
      }
      return result;
    },
    async getData() {
      // console.log('params is', this.$route.query);
      let _params = {
        'tid': this.$route.query.tid,
        'build_id': this.$route.query.build_id,
        'task_type': this.$route.query.task_type,
        'secondary_type': this.$route.query.secondary_type
      };
      // 自己知道自己值传递了一个secondary_type
      const { code, data, message } = await api.get(DetailUrl, _params);
      if (message === 'success') {
        for (let key in data) {
          if (data.hasOwnProperty(key)) {
            this.detail = data[key].case_detail;
            if (this.detail.length > 0) {
              this.env_info = this.pocessData(this.detail[0].env_info);
              this.compile_param = this.pocessData(this.detail[0].compile_param);
              this.gpu_arch = this.pocessData(this.detail[0].gpu_arch);
              this.gpu_arch.push({key: "artifact_url", value: this.$route.query.artifact_url});
            }
          }
        }
      } else {
        console.log('code: ', code);
        this.$Message.error({content: message || this.$trans('获取编译列表失败'), duration: 5, closable: true});
      }
    }
  }
};
</script>

<style scoped>
  .tips {
    color: #ff9900;
  }
  .all-line-row {
    margin-bottom: 0.5%;
    margin-left: 0.5%;
  }
  .center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 2%
  }
</style>

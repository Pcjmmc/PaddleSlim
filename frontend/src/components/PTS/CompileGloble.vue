<template>
  <div>
    <Card class="card-s-new">
      <div>
        <Form
          :model="search"
          :label-width="75"
          style="width: 85%"
        >
          <Row>
            <Col span="14">
              <FormItem label="时间:" prop="dt">
                <DatePicker
                  clearable
                  type="daterange"
                  placement="bottom-end"
                  placeholder=" 开始时间 ～ 结束时间 "
                  v-model="search.dt"
                  style="width:80%"
                  v-on:on-change="searchByfilters"
                ></DatePicker>
              </FormItem>
            </Col>
          </Row>
          <Row>
            <Col span="6">
             <FormItem label="系统:" prop="os">
                <Select clearable v-model="search.os">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in os"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="6">
              <FormItem
                label="分支:"
                prop="branch"
              >
                <Select clearable v-model="search.branch">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in branch"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="6">
              <FormItem label="CUDA:" prop="cuda">
                <Select clearable v-model="search.cuda">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in cuda"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
          </Row>
          <Row>
             <Col span="6">
              <FormItem label="Python:" prop="python">
                <Select clearable v-model="search.python">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in python"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="6">
              <FormItem label="类型:" prop="type">
                <Select clearable v-model="search.type">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in testType"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="8">
              <FormItem label="取值:" prop="value">
                <Input
                  clearable
                  v-model="search.value"
                  placeholder="输入 pr、commit 或 包地址"
                ></Input>
              </FormItem>
            </Col>
            <Col span="2" offset="1">
              <Button
                class="btn-success"
                shape="circle"
                icon="ios-search"
                @click="searchByfilters"
              >Search</Button>
            </Col>
          </Row>
        </Form>
      </div>
    </Card>
    <div>
      <Row>
        <Card
          :key="index"
          :id="index"
          class="card-css"
          v-for="(item, index) in envInfo"
        >
          <div>
            <Table
              border
              :show-header="false"
              :columns="envcolumns"
              :data="item"
            ></Table>
          </div>
        </Card>
      </Row>
    </div>
    <Page
      :total="total"
      :current="parseInt(page)"
      :page-size="parseInt(pagesize)"
      size="small"
      style="text-align: center;"
      v-on:on-change="pageChange"
      >
    </Page>
  </div>
</template>

<script>
import { dateFmt } from '../../util/help.js';
import { FrameWorkConfigUrl, FrameCompileSearchUrl } from '../../api/url.js';
import Clipboard from 'clipboard';
import api from '../../api/index';

export default {
  name: 'CompileService',
  data: function () {
    return {
      scale: 0.9,
      total: 0,
      page: 1,
      pagesize: 30,
      content: [
      ],
      envcolumns: [
        {
          title: '内容1',
          key: 'content1',
          align: 'center',
          render: (h, params) => {
            let ret = [];
            if (params.row.content1.indexOf('commit') !== -1) {
              ret.push(
                h('Tooltip', {
                  props: {
                    placement: 'right',
                    transfer: true
                  }
                }, [
                  h('div', {
                    style: {
                      width: '135px',
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                      textOverflow: 'ellipsis'
                    }
                  }, params.row.content1),
                  h('span', {
                    slot: 'content',
                    style: {
                      whiteSpace: 'normal',
                      wordBreak: 'break-all'
                    }
                  }, params.row.content1)
                ])
              );
            } else {
              ret.push(
                h(
                  'div',
                  {
                  }, params.row.content1
                )
              );
            }
            return h(
              'div',
              {
                style: {
                  align: 'center'
                }
              },
              ret
            );
          }
        },
        {
          title: '内容2',
          key: 'content2',
          align: 'center',
          render: (h, params) => {
            let ret = [];
            let str1 = '产物地址 :';
            if (params.row.content2.indexOf(str1) === -1) {
              ret.push(
                h(
                  'div',
                  {
                  }, params.row.content2
                )
              );
            } else {
              let url = params.row.content2.substr(str1.length);
              ret.push(h('span', [
                h('span', {
                }, str1),
                h('a', {
                  }),
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
              ret.push(h('span', [
                h('a', {
                  }),
                  h('Poptip', {
                    props: {
                      trigger: 'hover',
                      placement: 'top',
                      transfer: true,
                      content: '下载'
                    }
                  },
                  [
                    h('Icon', {
                      props: {
                          type: 'md-arrow-down',
                          size: '20',
                          color: 'gray'
                      },
                      on: {
                        click: () => {
                          window.open(url, '_self');
                        }
                      }
                    })
                  ])
                ])
              );
            }
            return h(
              'div',
              {
                style: {
                  align: 'center'
                }
              },
              ret
            );
          }
        }
      ],
      orders: [
        [
          'os',
          'branch'
        ],
        [
          'python',
          'cuda'
        ],
        [
          'type',
          'wheel'
        ]
      ],
      search: {
        dt: [],
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: ''
      },
      branch: [
      ],
      cuda: [
      ],
      os: [
      ],
      python: [
      ],
      testType: [
      ]
    };
  },
  watch: {
  },
  mounted: async function () {
    this.initData();
    await this.getConfigs();
    await this.getData();
  },
  components: {
  },
  computed: {
    envInfo: {
      get() {
        let info = [];
        for (let i = 0; i < this.content.length; i++) {
          let arr = [];
          let tmp = JSON.parse(this.content[i].env);
          tmp.wheel = this.content[i].wheel;
          for (let j = 0; j < this.orders.length; j++) {
            let key1 = this.orders[j][0];
            let key2 = null;
            let content1 = '';
            if (key1 === 'type' && tmp[key1] !== 'wheel') {
              content1 = tmp[key1] + ' : ' + tmp.value;
            } else {
              content1 = this.getKeysDesc(key1) + ' : ' + tmp[key1];
            }
            let content2 = null;
            if (this.orders[j].length === 2) {
              key2 = this.orders[j][1];
              content2 = this.getKeysDesc(key2) + ' : ' + tmp[key2];
            }
            let cons = {
              content1: content1,
              content2: content2
            };
            arr.push(cons);
          }
          info.push(arr);
        }
        return info;
      }
    }
  },
  methods: {
    copyData(url) {
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
    },
    initData() {
      this.content = [];
      this.page = 1;
      this.search = {
        dt: [],
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: ''
      };
    },
    inFun(idx) {
      this.scale = 1;
      document.getElementById(idx).style = `transform:scale(${this.scale})`;
    },
    outFun(idx) {
      this.scale = 0.9;
      document.getElementById(idx).style = `transform:scale(${this.scale})`;
    },
    getKeysDesc(item) {
      switch (item.toLowerCase()) {
        case 'os':
          return '系统';
        case 'python':
          return 'Py环境';
        case 'cuda':
          return 'CUDA环境';
        case 'branch':
          return '分支';
        case 'wheel':
          return '产物地址';
        case 'type':
          return '类型';
        default:
          return item;
      }
    },
    async getConfigs() {
      const {code, data, message} = await api.get(FrameWorkConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.branch = data.compile_branch;
        this.cuda = data.compile_cuda;
        this.os = data.compile_os;
        // 先把这些推荐去
        this.os.push('Windows');
        this.os.push('Mac');
        this.python = data.compile_python;
        this.testType = data.compile_type;
      } else {
        this.branch = [];
        this.cuda = [];
        this.os = [];
        this.python = [];
        this.testType = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      this.content = [];
      let begin_time = null;
      let end_time = null;
      if (this.search.dt[0]) {
        begin_time = dateFmt(this.search.dt[0], 'yyyy-MM-dd');
      }
      if (this.search.dt[1]) {
        // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
        end_time = new Date(this.search.dt[1]);
        end_time = end_time.setDate(end_time.getDate() + 1);
        end_time = new Date(end_time);
        end_time = dateFmt(end_time, 'yyyy-MM-dd');
      }
      let params = {
        page_index: this.page,
        limit: this.pagesize,
        begin_time: begin_time,
        end_time: end_time,
        status: 'done',
        pd_type: this.search.type,
        value: this.search.value,
        cuda: this.search.cuda,
        branch: this.search.branch,
        os: this.search.os,
        python: this.search.python
      };
      const {code, data, message, all_count} = await api.get(FrameCompileSearchUrl, params);
      if (parseInt(code, 10) === 200) {
        this.content = data;
        this.total = all_count;
      } else {
        this.content = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async searchByfilters() {
      this.page = 1;
      await this.getData();
    },
    async pageChange(pageNum) {
      this.page = pageNum;
      await this.getData();
    }
  }
};
</script>

<style scoped>
.card-s-new {
  width: 100%;
  font-size: 14px;
  color: lightslategrey
}
.ivu-form-item{
  margin-bottom: 12px;
  font-size: 14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.card-css {
  width: 33%;
  margin-top: 1%;
  text-align: center;
  font-size: 14px;
}
</style>
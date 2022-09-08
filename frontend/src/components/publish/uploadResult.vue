<template>
  <div style="margin-left:2%;margin-right:2%;">
    <Table
      :columns="columns"
      :data="data"
      border
    >
    </Table>
  </div>
</template>
<script>
import Cookies from 'js-cookie';
import api from '../../api/index';
import { PublishResult } from '../../api/url.js';

export default {
  data() {
    return {
      columns: [
        {
          title: '发布源',
          key: 'source',
          width: "100px",
          align: "center"
        },
        {
          title: '发布内容',
          align: "center",
          key: 'content',
          render: (h, {row, index}) => {
            let edit;
            let control;
            if (this.editIndex === index) {
              edit = [h('Input', {
                props: {
                  value: row.content
                },
                on: {
                  input: (val) => {
                    this.editValue = val;
                  }
                }
              })];
              control = [
                h('Icon', {
                  style: {
                    cursor: 'pointer',
                    margin: '8px'
                  },
                  props: {
                    type: 'md-checkmark',
                    size: 16,
                    color: '#19be6b'
                  },
                  on: {
                    click: () => {
                      this.data[index].content = this.editValue;
                      this.changeData(this.data[index]);
                      this.editIndex = -1;
                    }
                  }
                })
              ]
            } else {
              edit = row.content;
              control = [h('Icon', {
                style: {
                  cursor: 'pointer'
                },
                props: {
                  type: 'ios-create-outline',
                  size: 16
                },
                on: {
                  click: () => {
                    this.editIndex = index;
                    this.editValue = row.content;
                  }
                }
              })]
            }
            return h('Row', [
              h('Col', {
                props: {
                  span: 22
                }
              }, edit),
              h('Col', {
                props: {
                  span: 2
                }
              }, control)
            ])
          }
        },
        {
          title: '地址',
          align: "center",
          key: 'url',
          render: (h, {row, index}) => {
            let edit;
            let control;
            if (this.editUrlIndex === index) {
              edit = [h('Input', {
                props: {
                  value: row.url
                },
                on: {
                  input: (val) => {
                    this.editUrl = val;
                  }
                }
              })];
              control = [
                h('Icon', {
                  style: {
                    cursor: 'pointer',
                    margin: '8px'
                  },
                  props: {
                    type: 'md-checkmark',
                    size: 16,
                    color: '#19be6b'
                  },
                  on: {
                    click: () => {
                      this.data[index].url = this.editUrl;
                      this.changeData(this.data[index]);
                      this.editUrlIndex = -1;
                    }
                  }
                })
              ]
            } else {
              edit = row.url;
              control = [h('Icon', {
                style: {
                  cursor: 'pointer'
                },
                props: {
                  type: 'ios-create-outline',
                  size: 16
                },
                on: {
                  click: () => {
                    this.editUrlIndex = index;
                    this.editUrl = row.url;
                  }
                }
              })]
            }
            return h('Row', [
              h('Col', {
                props: {
                  span: 22
                }
              }, edit),
              h('Col', {
                props: {
                  span: 2
                }
              }, control)
            ])
          }
        }
      ],
      data: [],
      editIndex: -1,
      editValue: '',
      editUrlIndex: -1,
      editUrl: ''
    }
  },
  computed: {
    version: {
      get() {
        if (this.$route.query.version) {
          // 将url中的版本优先
          return this.$route.query.version;
        } else {
          return this.$store.state.version;
        }
      }
    }
  },
  methods: {
    async getData() {
      // 根据需求实时获取; 后台根据version获取到计划tag
      let params = {
        tag: this.version
      };
      const {code, data, message, all_count} = await api.get(PublishResult, params);
      if (parseInt(code, 10) === 200) {
        // 将data中的覆盖到tmpData
        this.data = data;
      } else {
        this.data = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async changeData(row) {
      // 如果有id则更新；否则则新增
      if (row.id) {
        await this.updateData(row);
      } else {
        await this.createData(row);
      }
      await this.getData();
    },
    async updateData(row) {
      let params = {
        tag: this.version,
        source: row.source,
        content: row.content,
        url: row.url,
        id: row.id
      };
      await api.put(PublishResult, params);
    },
    async createData(row) {
      let params = {
        tag: this.version,
        source: row.source,
        content: row.content,
        url: row.url
      };
      await api.post(PublishResult, params);
    }
  },
  watch: {
    version: function () {
      this.getData();
    }
  },
  mounted() {
    this.getData();
  }
}
</script>

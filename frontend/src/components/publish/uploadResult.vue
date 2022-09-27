<template>
  <div style="margin-left:1%;margin-right:1%;">
    <Table
      :columns="columns"
      :data="data"
      border
      :span-method="handleSpan"
    ></Table>
  </div>
</template>
<script>
import Clipboard from 'clipboard';
import api from '../../api/index';
import { PublishResult } from '../../api/url.js';

export default {
  data() {
    return {
      columns: [
        {
          title: '发布源',
          key: 'source',
          width: '200px',
          align: 'center',
          render: (h, params) => {
            let name = params.row.source;
            let jumUrl = this.getUrl(name);
            if (jumUrl) {
              return h('div', [
                h('a', {
                  href: 'javascript:void(0);',
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.jumper(jumUrl);
                    }
                  }
                }, params.row.source)
              ]);
            } else {
               return h('div', [
                h('span', {
                }, params.row.source)
              ]);
            }
          }
        },
        {
          title: '环境',
          key: 'system',
          width: '200px',
          align: 'center'
        },
        {
          title: '内容',
          key: 'content',
          align: 'center',
          render: (h, params) => {
            let ret = [];
            let content = params.row.content;
            let _this = this; // this跟循环里面相冲突
            Object.keys(content).forEach(function (key) {
              let item = content[key];
              ret.push(
                h(
                  'span',
                  {
                    style: {
                      marginRight: '10px',
                      fontWeight: 'bold'
                    }
                  },
                  key + ':'
                )
              );
              item.forEach(element => {
                let desc = element.desc;
                let url = element.url;
                if (url) {
                  ret.push(
                    h('a', {
                      href: 'javascript:void(0);',
                      on: {
                        click: () => {
                          _this.jumper(url);
                        }
                      }
                    }, desc)
                  );
                  ret.push(
                    h('Poptip', {
                      props: {
                        trigger: 'hover',
                        placement: 'top',
                        // 注意一定要添加该属性，否则表格会遮盖住气泡浮框
                        transfer: true,
                        content: '复制地址'
                      },
                      style: {
                        marginRight: '10px'
                      }
                    },
                    [
                      h('Icon', {
                        class: 'ivu-icon ivu-icon-ios-copy-outline copyBtn',
                        props: {
                            type: 'ios-copy-outline',
                            size: '15',
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
                              _this.$Message.success('复制成功~');
                              e.clearSelection();
                            });
                            clipboard.on('error', e => {
                              _this.$Message.error('复制失败,请手动复制~');
                            });
                          }
                        }
                      })
                    ])
                  );
                } else {
                  ret.push(
                    h('span', {
                      style: {
                        marginLeft: '10px'
                      }
                    }, desc)
                  );
                }
              });
            });
            return h(
              'div',
              {
                style: {
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'flex-start',
                  alignItems: 'flex-start'
                }
              },
              ret
            );
          }
        }
      ],
      data: []
    };
  },
  watch: {
    versionName: function () {
      this.getData();
    }
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    handleSpan({ row, column, rowIndex, columnIndex }) {
      // 合并第二列,这里columnIndex===1 根据具体业务来，比如本示例中需要合并的source为第二列
      if (columnIndex === 0) {
        // 计算合并的行数列数
        let x = row.mergeCol === 0 ? 0 : row.mergeCol;
        let y = row.mergeCol === 0 ? 0 : 1;
        return [x, y];
      }
      // system 合并
      if (columnIndex === 1) {
        // 计算合并的行数列数
        let x = row.mergeColSystem === 0 ? 0 : row.mergeColSystem;
        let y = row.mergeColSystem === 0 ? 0 : 1;
        return [x, y];
      }
    },
    formatData(data) {
      let names = [];
      // 筛选出不重复的 source,将其放到 names数组中
      data.forEach((e) => {
        if (!names.includes(e.source)) {
          names.push(e.source);
        }
      });

      let nameNums = [];
      // 将names数组中的 name值设置默认合并0个单元格,放到 nameNums中
      names.forEach((e) => {
        nameNums.push({ source: e, num: 0 });
      });

      // 计算每种 name值所在行需要合并的单元格数
      data.forEach((e) => {
        nameNums.forEach((n) => {
          if (e.source === n.source) {
            n.num++;
          }
        });
      });
      // 将计算后的合并单元格数整合到 data中
      data.forEach((e) => {
        nameNums.forEach((n) => {
          if (e.source === n.source) {
            if (names.includes(e.source)) {
              e.mergeCol = n.num;
              // 删除已经设置过的值(防止被合并的单元格进到这个 if 语句中)
              names.splice(names.indexOf(n.source), 1);
            } else {
              // 被合并的单元格设置为 0
              e.mergeCol = 0;
            }
          }
        });
      });
      // 不唯一且重复的情况下，在唯一的基础上合并重复
      for (let j = 0; j < data.length; j++) {
        //  > 1 name 表示 有合并需要在name合并的row中 再合并
        if (data[j].mergeCol > 1) {
          for (let k = 0; k < data[j].mergeCol; k++) {
            // age合并
            if (data[j + k].systemAlready !== 1) { // 需要这个条件，避免数据重复
              if (k + 1 < data[j].mergeCol) {
                data[j + k].mergeColSystem = 1;
                for (let b = k + 1; b < data[j].mergeCol; b++) {
                  if (data[j + k].system === data[j + b].system) {
                    data[j + k].mergeColSystem++;
                    data[j + b].mergeColSystem = 0;
                    data[j + b].systemAlready = 1;
                  } else {
                    break;
                  }
                }
              }
            }
          }
        }
      }
      return data;
    },
    async getData() {
      // 根据需求实时获取; 后台根据version获取到计划tag
      if (!this.versionName) {
        return;
      }
      let params = {
        version: this.versionName
      };
      const {code, data, message} = await api.get(PublishResult, params);
      if (parseInt(code, 10) === 200) {
        // 将data中的覆盖到tmpData
        this.data = this.formatData(data);
      } else {
        this.data = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    jumper(href) {
      window.open(href, '_blank');
    },
    getUrl(name) {
      let tmp = this.versionName.split('v');
      let v = null;
      if (tmp.length === 2) {
        v = tmp[1];
        v = v.replace('-', '');
      } else {
        return null;
      }
      switch (name.toLowerCase()) {
        case 'docker':
          return `https://hub.docker.com/r/paddlepaddle/paddle/tags?page=1&name=${v}`;
        case 'conda':
          return `https://anaconda.org/Paddle/paddlepaddle-gpu/files?version=${v}`;
        case 'pypi':
          return `https://pypi.org/project/paddlepaddle-gpu/${v}/#files`;
      }
    }
  },
  mounted() {
    this.getData();
  }
};
</script>

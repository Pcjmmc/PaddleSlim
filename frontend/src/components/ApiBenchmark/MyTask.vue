<template>
  <div class="center-card-s">
    <div style="margin-top: 2%">
      <div style="cursor: pointer">
        任务状态：
        <span v-for="(item, index) in tags">
          <span v-if="item.checked">
            <Tag
              :checked="item.checked"
              color="primary"
              v-on:on-change="changeTagStatus(item)"
            >
              <p style="font-size: 14px">{{ item.desc }}</p>
            </Tag>
          </span>
          <span v-else>
            <Tag
              checkable
              :checked="item.checked"
              color="primary"
              v-on:on-change="changeTagStatus(item)"
            >
              <p style="font-size: 14px">{{ item.desc }}</p>
            </Tag>
          </span>
        </span>
      </div>
    </div>
    <div style="margin-top: 2%">
      <span>
        创建时间:
        <DatePicker
          type="daterange"
          placement="bottom-end"
          placeholder=" 开始时间 ～ 结束时间 "
          style="width: 30%"
          v-model="dt"
          v-on:on-change="searchByfilter"
        ></DatePicker>
      </span>
    </div>
    <div style="margin-top: 2%">
      <div>
        任务ID:
        <Input
          v-model="search.id"
          placeholder="任务ID"
          style="width: 150px"
        >
        </Input>
        任务名:
        <Input
          v-model="search.name"
          placeholder="任务名"
          style="width: 300px"
        >
      </Input>
        <Button
          class="btn-success"
          shape="circle"
          icon="ios-search"
          @click="searchByfilter"
        >
        Search
        </Button>
      </div>
      <div style="text-align: right">
        <Button
          icon="md-add"
          class="btn-success"
          @click="createNewJob"
        >
          新建测试任务
        </Button>
        <Button
          icon="md-"
          class="btn-success"
          @click="getComporeReport"
        >
          查看对比
        </Button>
      </div>
    </div>
    <div style="margin-top: 2%">
      <div class="left" style="margin-top: 2%">
        <Table
        border
        :columns="columns"
        :data="content"
        v-on:on-select="selectTable"
        v-on:on-select-cancel="selectCancel"
        >
      </Table>
        <Page
          :total="total"
          :current="parseInt(search.page)"
          :page-size="parseInt(search.pagesize)"
          size="small"
          style="text-align: center"
          v-on:on-change="pageChange"
        >
        </Page>
      </div>
    </div>
    <Modal
      v-model="showModa"
      title="创建测试任务"
      width="30%"
    >
      <benchmark-exec
        ref="child"
        @closeModal="closeModal"
        @searchByfilter="searchByfilter"
      > </benchmark-exec>
      <div slot="footer">
        <Button
          type="text"
          @click="handleReset"
        >
          重置
        </Button>
        <Button
          type="primary"
          @click="handleSubmit"
        >
          提交
        </Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import { ApiBenchmarkTaskList, ApiBenchmarkRoutine, ApiBenchmarkSetBaseline } from '../../api/url';
import api from '../../api/index';
import { dateFmt } from '../../util/help.js';
import BenchmarkExec from './BenchmarkExec.vue';
export default {
  name: 'ApiBenchmarkExec',
  data: function () {
    return {
      showModa: false,
      selection: [

      ],
      tags: [
        {
          id: 'all',
          desc: '全部',
          checked: true
        },
        {
          id: 'prepare',
          desc: '准备中',
          checked: false
        },
        {
          id: 'running',
          desc: '运行中',
          checked: false
        },
        {
          id: 'done',
          desc: '已完成',
          checked: false
        },
        {
          id: 'error',
          desc: '异常',
          checked: false
        }
      ],
      columns: [
        {
          type: 'selection',
          width: 60,
          align: 'center',
          fixed: 'left'
        },
        {
          title: '任务ID',
          key: 'id',
          align: 'center',
          fixed: 'left',
          minWidth: 100
        },
        {
          title: '任务名',
          key: 'comment',
          align: 'center',
          minWidth: 100
        },
        {
          title: '任务状态',
          key: 'status',
          align: 'center',
          minWidth: 100,
          render: (h, params) => {
              return h('div', [
                  h('p', {
                    style: {
                      color: this.setStatusColor(params.row.status)
                    }
                  }, params.row.status)
              ]);
          }
        },
        {
          title: 'Framework',
          key: 'framework',
          align: 'center',
          minWidth: 120
        },
        {
          title: 'Python',
          key: 'python',
          align: 'center',
          minWidth: 100
        },
        {
          title: 'OS',
          key: 'system',
          align: 'center',
          minWidth: 100
        },
        {
          title: 'Place',
          key: 'place',
          align: 'center',
          minWidth: 100
        },
        {
          title: 'CUDA',
          key: 'cuda',
          align: 'center',
          minWidth: 100
        },
        {
          title: '反向',
          key: 'enable_backward',
          align: 'center',
          minWidth: 100,
          render: (h, params) => {
              return h('div', [
                  h('p', {
                  }, this.setBackward(params.row))
              ]);
          }
        },
        {
          title: '配置详情',
          align: 'center',
          minWidth: 100,
          render: (h, params) => {
            let str = this.setDefaultConfig(params.row.yaml_info);
            return h('div', [
                    h('p', {
                    }, str)
                ]);
          }
        },
        {
          title: '版本信息',
          key: 'version',
          align: 'center',
          minWidth: 100,
          render: (h, params) => {
            if (params.row.wheel_link !== null) {
              return h('div', [
                    h('Button', {
                      props: {
                        to: params.row.wheel_link,
                        target: '_blank',
                        icon: 'ios-download-outline'
                      }
                    })
                ]);
            } else {
              return h('div', [
                    h('p', {
                    }, params.row)
                ]);
            }
          }
        },
        {
          title: '创建时间',
          key: 'create_time',
          align: 'center',
          minWidth: 120
        },
        {
          title: '操作',
          key: 'detail',
          align: 'center',
          fixed: 'right',
          minWidth: 160,
          render: (h, params) => {
            return h('div', [
              h(
                'Button',
                {
                  props: {
                    disabled: this.setDisabled(params.row)
                  },
                  on: {
                    click: () => {
                      this.getReport(params.row);
                    }
                  }
                },
                '查看报告'
              ),
              h(
                'Button',
                {
                  props: {
                    icon: this.setBaselineIcon(params.row)
                  },
                  on: {
                    click: () => {
                      this.setBaseline(params.row);
                    }
                  }
                }
              )
            ]);
          }
        }
      ],
      total: 0,
      content: [
      ],
      dt: [this.getBeginData(), new Date()],
      search: {
        comment: '',
        id: null,
        status: 'all',
        begin_time: null,
        end_time: null,
        page: 1,
        pagesize: 15
      }
    };
  },
  mounted: function () {
    this.initData();
    this.searchByfilter();
  },
  methods: {
    initData() {
      this.tableSelect = [];
      this.content = [];
      this.search = {
        comment: '',
        id: null,
        begin_time: null,
        end_time: null,
        status: 'all',
        page: 1,
        pagesize: 15
      };
    },
    setStatusColor(value) {
      if (value === 'done') {
        return 'green';
      } else if (value === 'error') {
        return 'red';
      }
    },
    getBeginData() {
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let begin_time = new Date();
      begin_time = begin_time.setDate(begin_time.getDate() - 7);
      begin_time = new Date(begin_time);
      return begin_time;
    },
    setBackward(row) {
      if (row.enable_backward === 0) {
        return '是';
      } else {
        return '否';
      }
    },
    setDefaultConfig(value) {
      if (value === 'case_0') {
        return '小kernel';
      } else if (value === 'case_1') {
        return '中kernel';
      } else if (value === 'case_2') {
        return '大kernel';
      } else {
        return '全部kernel';
      }
    },
    setDisabled(row) {
      if (row.status === 'done') {
        return false;
      } else {
        return true;
      }
    },
    async setBaseline(row) {
      if (row.routine === 0) {
        let params = {
          id: row.id,
          routine: 1
        };
        const {code, message, data} = await api.post(ApiBenchmarkSetBaseline, params);
        if (parseInt(code, 10) === 200) {
          this.searchData();
        } else {
          this.$Message.error({
            content: '设置基线失败' + message,
            duration: 1,
            closable: true
          });
        }
      } else {
        let params = {
          id: row.id,
          routine: 0
        };
        const {code, message, data} = await api.post(ApiBenchmarkSetBaseline, params);
        if (parseInt(code, 10) === 200) {
          this.searchData();
        } else {
          this.$Message.error({
            content: '取消基线失败' + message,
            duration: 1,
            closable: true
          });
        }
      }
    },
    setBaselineIcon(row) {
      if (row.routine === 0) {
        return 'md-star-outline';
      } else {
        return 'md-star';
      }
    },
    async getReport(row) {
      const {code, data, message, _} = await api.get(ApiBenchmarkRoutine);
      if (parseInt(code, 10) === 200) {
          let _params = {
          id: row.id,
          id1: data.id
        };
        const { href } = this.$router.resolve({name: 'ApiBenchmarkBaseReport', params: _params});
        window.open(href, '_blank');
      } else {
        this.content = [];
        this.$Message.error({
          content: '未找到可以对比的基线 ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    getComporeReport() {
      if (this.selection.length !== 2) {
        this.$Message.error({
          content: '请选择两个版本进行对比',
          duration: 1,
          closable: true
        });
      } else {
        let _params = {
          id: this.selection[0].id,
          id1: this.selection[1].id
        };
        const { href } = this.$router.resolve({name: 'ApiBenchmarkBaseReport', params: _params});
        window.open(href, '_blank');
      }
    },
    async searchByfilter() {
      this.search.page = 1;
      await this.searchData();
    },
    async changeTagStatus(item) {
      this.$set(item, 'checked', true);
      // 将选中以外的设置成false
      for (let i = 0; i < this.tags.length; i++) {
        let id = this.tags[i].id;
        if (id !== item.id) {
          this.tags[i].checked = false;
        } else {
          this.$set(this.tags[i], 'checked', true);
          this.tags[i].checked = true;
          this.search.status = this.tags[i].id;
        }
      }
      await this.searchByfilter();
    },
    async createNewJob() {
      this.showModa = true;
    },
    async handleReset() {
      await this.$refs.child.initData();
    },
    async handleSubmit() {
      await this.$refs.child.handleSummit();
    },
    closeModal(params) {
      this.showModa = params;
    },
    async pageChange(pageNum) {
      this.search.page = pageNum;
      await this.searchData();
    },
    async searchData() {
      // 根据条件查询
      this.content = [];
      this.search.begin_time = dateFmt(this.dt[0], 'yyyy-MM-dd');
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let end_time = new Date(this.dt[1]);
      end_time = end_time.setDate(end_time.getDate() + 1);
      end_time = new Date(end_time);
      this.search.end_time = dateFmt(end_time, 'yyyy-MM-dd');
      let params = {
        page_index: this.search.page,
        limit: this.search.pagesize,
        begin_time: this.search.begin_time,
        end_time: this.search.end_time,
        id: this.search.id ? this.search.id : null,
        comment: this.search.name ? this.search.name : null,
        status: this.search.status === 'all' ? null : this.search.status
      };
      // 如果根据任务id或者任务名检索的话，就不需要加其他条件？？？
      const {code, data, message, all_count} = await api.get(ApiBenchmarkTaskList, params);
      if (parseInt(code, 10) === 200) {
        this.content = data;
        this.addSpecialProp();
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
    addSpecialProp() {
      for (let i in this.content) {
        let row = this.content[i];
        if (row.status === 'done') {
          this.content[i]._disabled = false;
        } else {
          this.content[i]._disabled = true;
        }
      }
    },
    selectTable(selection) {
      this.selection = selection;
      if (selection.length > 2) {
        this.$Message.error({
          content: '只能选择两个版本进行对比',
          duration: 1,
          closable: true
        });
      }
    },
    selectCancel(selection) {
      this.selection = selection;
    }
  },
  components: { BenchmarkExec }
};
</script>

<style scoped>
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.center-card-s {
  margin-left: 1%;
  margin-right: 1%;
  font-size: 14px;
  color: lightslategrey;
}
</style>

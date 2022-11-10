<template>
  <div>
    <Card class="center-card-s">
      <div style="margin-top: 1%;">
        <div style="cursor:pointer;">
          任务状态:
            <span v-for="item, index in tags">
              <span v-if="item.checked">
                <Tag
                  border
                  :checked="item.checked"
                  color="primary"
                  v-on:on-change="changeTagStatus(item)"
                >
                  <font size="3"> {{ item.desc }}</font>
                </Tag>
              </span>
              <span v-else>
                <Tag
                  border
                  checkable
                  :checked="item.checked"
                  color="primary"
                  v-on:on-change="changeTagStatus(item)"
                >
                  <font size="3"> {{ item.desc }}</font>
                </Tag>
              </span>
            </span>
        </div>
      </div>
      <div style="margin-top: 2%;">
        <span>
          创建时间:
          <DatePicker
            type="daterange"
            placement="bottom-end"
            placeholder=" 开始时间 ～ 结束时间 "
            v-model="dt"
            style="width:30%"
            v-on:on-change="searchByfilter"
          ></DatePicker>
        </span>
      </div>
      <div style="margin-top: 2%;">
        <div class="left">
          任务ID:
          <Input
            v-model="search.id"
            placeholder="任务ID"
            style="width:150px;"
          ></Input>
          任务名:
          <Input
            v-model="search.name"
            placeholder="任务名"
            style="width:300px;"
          ></Input>
          <Button
            type="primary"
            shape="circle"
            icon="ios-search"
            @click="searchByfilter"
          >Search</Button>
        </div>
        <div class="right">
          <Button
            icon="md-add"
            type="primary"
            @click="createNewJob"
          >新建测试任务</Button>
        </div>
      </div>
      <div style="margin-top: 2%;">
        <div class="left" style="margin-top: 2%;">
          <Table
            border
            :columns="columns"
            :data="content"
          ></Table>
          <Page
            :total="total"
            :current="parseInt(search.page)"
            :page-size="parseInt(search.pagesize)"
            size="small"
            style="text-align: center;"
            v-on:on-change="pageChange"
            >
          </Page>
        </div>
      </div>
    </Card>
    <Modal
      v-model="showModa"
      title="创建测试任务"
      width="60%"
      v-on:on-cancel="handleReset"
    >
      <test-job
        ref="child"
        @closeModal="closeModal"
        @searchByfilter="searchByfilter"
        @SubmitRequirement="SubmitRequirement"
      ></test-job>
      <div slot="footer">
        <Button type="text" @click="handleReset">重置</Button>
        <Button type="primary" @click="handleSubmit">提交</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
// import Cookies from 'js-cookie';
import api from '../../api/index';
import { dateFmt } from '../../util/help.js';
import { FrameWorkJobListUrl } from '../../api/url.js';
import TestJob from './TestJob.vue';

export default {
  name: 'CompileService',
  data: function () {
    return {
      showModa: false,
      tags: [
        {
          id: 'all',
          desc: '全部',
          checked: true
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
      total: 0,
      content: [
      ],
      columns: [
        {
          title: '任务ID',
          key: 'id',
          align: 'center'
        },
        {
          title: '任务名',
          key: 'description',
          align: 'center'
        },
        {
          title: '任务状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Tag', {
                props: {
                  color: this.setColor(params.row.status)
                },
                style: {
                  width: '100px'
                }
              }, this.getStatus(params.row.status))
            ]);
          }
        },
        {
          title: '创建时间',
          key: 'create_time',
          align: 'center'
        },
        {
          title: '更新时间',
          key: 'update_time',
          align: 'center'
        },
        {
          title: '详情',
          key: 'detail',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'info'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleDetail(params.row);
                  }
                }
              }, '查看详情')
            ]);
          }
        }
      ],
      dt: [new Date(), new Date()],
      search: {
        name: '',
        id: null,
        status: 'all',
        begin_time: null,
        end_time: null,
        page: 1,
        pagesize: 10
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.initData();
    this.searchByfilter();
  },
  components: {
    TestJob
  },
  computed: {
  },
  methods: {
    getStatus(status) {
      for (let i = 0; i <= this.tags.length; i++) {
        let item = this.tags[i];
        if (item.id === status) {
          return item.desc;
        }
      }
      return status;
    },
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'done':
          return 'success';
        case 'success':
          return 'success';
        case 'passed':
          return 'success';
        case 'pass':
          return 'success';
        case 'running':
          return 'primary';
        case 'warning':
          return 'warning';
        case 'error':
          return 'warning';
        case 'fail':
          return 'error';
        case 'failed':
          return 'error';
        default:
          return 'error';
      }
    },
    handleDetail(row) {
      let _params = {
        jid: row.id
      };
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'SingleDetail', params: _params});
      window.open(href, '_blank');
    },
    async handleReset() {
      await this.$refs.child.initData();
    },
    async handleSubmit() {
      await this.$refs.child.handleSubmit();
    },
    async pageChange(pageNum) {
      this.search.page = pageNum;
      await this.searchData();
    },
    closeModal(params) {
      // 关闭弹窗
      this.showModa = params;
    },
    initData() {
      this.content = [];
      this.search = {
        name: '',
        id: null,
        begin_time: null,
        end_time: null,
        status: 'all',
        page: 1,
        pagesize: 10
      };
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
    async searchByfilter() {
      this.search.page = 1;
      await this.searchData();
    },
    async SubmitRequirement(jid) {
      // 什么也无需做，只是保持格式统一
      console.log('return jid is', jid);
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
        description: this.search.name ? this.search.name : null,
        status: this.search.status === 'all' ? null : this.search.status
      };
      // 如果根据任务id或者任务名检索的话，就不需要加其他条件？？？
      const {code, data, message, all_count} = await api.get(FrameWorkJobListUrl, params);
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
    }
  }
};
</script>

<style scoped>
.left{
  float:left;
}
.right{
float:right;
margin-right: 5%;
}
.demo-split{
  height: 861px;
  overflow:auto;
}
.modacss{
  width: 80%;
}
.demo-split-pane{
  padding: 10px;
  text-align:center
}
.demo-tree {
  width: 100%;
  line-height: 2;
}
.one-fifth-video-col {
  margin-right: 2px;
  margin-left: 2px;
  margin-bottom: 2px;
  margin-top: 2px;
}
.center-card-s {
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  min-height: 100px;
  overflow: auto;
  font-size: 16px;
  color:lightslategrey
}
.main {
  color:lightslategrey;
  margin-left: 1%;
  margin-bottom: 2%;
  font-size: 18px;
  align: center;
}
.all-line-row {
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 2%;
  margin-top: 1%;
}
</style>

<style>
.ivu-tree ul {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 20px;
}
.ivu-tree-title {
  display: inline-block;
  margin: 0;
  padding: 0 4px;
  border-radius: 3px;
  cursor: pointer;
  vertical-align: top;
  -webkit-transition: all .2s ease-in-out;
  transition: all .2s ease-in-out;
}
</style>
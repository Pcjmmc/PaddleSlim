<template>
  <div>
    <Card class="center-card-s">
      <div style="margin-top: 1%;">
        <span>
          任务状态:
            <span v-for="item, index in tags">
              <span v-if="item.checked">
                <Tag
                  :checked="item.checked"
                  color="primary"
                  v-on:on-change="changeTagStatus(item)"
                >
                  <font size="3"> {{ item.desc }}</font>
                </Tag>
              </span>
              <span v-else>
                <Tag
                  checkable
                  :checked="item.checked"
                  color="primary"
                  v-on:on-change="changeTagStatus(item)"
                >
                  <font size="3"> {{ item.desc }}</font>
                </Tag>
              </span>
            </span>
        </span>
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
          <Input
            v-model="search.jid"
            search
            suffix="ios-search"
            placeholder="任务ID"
            style="width:300px;"
            v-on:on-search="searchByfilter"
          ></Input>
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
      <test-job ref="child" @closeModal="closeModal"> </test-job>
      <div slot="footer">
        <Button type="text" @click="handleReset">重置</Button>
        <Button type="primary" @click="handleSubmit">提交</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
// import Cookies from 'js-cookie';
// import api from '../../api/index';
import { dateFmt } from '../../util/help.js';
import TestJob from './TestJob.vue';

export default {
  name: 'CompileService',
  data: function () {
    return {
      showModa: false,
      tags: [
        {
          id: '1',
          desc: '全部',
          checked: true
        },
        {
          id: '2',
          desc: '测试中',
          checked: false
        },
        {
          id: '3',
          desc: '测试通过',
          checked: false
        },
        {
          id: '4',
          desc: '测试失败',
          checked: false
        }
      ],
      total: 0,
      content: [
      ],
      columns: [
        {
          title: '任务ID',
          key: 'jid',
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
              h('p', {
                style: {
                  marginRight: '5px',
                  color: this.setColor(params.row.status)
                }
              }, params.row.status)
            ]);
          }
        },
        {
          title: '创建时间',
          key: 'create_time',
          align: 'center'
        },
        {
          title: '完成时间',
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
        jid: null,
        status: '全部',
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
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'done':
          return 'green';
        case 'success':
          return 'green';
        case 'passed':
          return 'green';
        case 'pass':
          return 'green';
        case 'warning':
          return 'yellow';
        case 'error':
          return 'red';
        case 'fail':
          return 'red';
        case 'failed':
          return 'red';
        default:
          return 'red';
      }
    },
    handleDetail(row) {
      let _params = {
        jid: row.jid
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
      this.page = pageNum;
      await this.searchByfilter();
    },
    closeModal(params) {
      // 关闭弹窗
      this.showModa = params;
    },
    initData() {
      this.content = [];
      this.search = {
        jid: null,
        begin_time: null,
        end_time: null,
        status: '全部',
        page: 1,
        pagesize: 10
      };
    },
    async changeTagStatus(item) {
      this.$set(item, 'checked', true);
      // 将选中以外的设置成false
      for (let i = 0; i < this.tags.length; i++) {
        let id = this.tags[i].id;
        if (parseInt(id, 10) !== parseInt(item.id, 10)) {
          this.tags[i].checked = false;
        } else {
          this.$set(this.tags[i], 'checked', true);
          this.tags[i].checked = true;
          this.search.status = this.tags[i].desc;
        }
      }
      await this.searchByfilter();
    },
    async createNewJob() {
      this.showModa = true;
    },
    async searchByfilter() {
      // 根据条件查询
      this.search.begin_time = dateFmt(this.dt[0], 'yyyy-MM-dd');
      this.search.end_time = dateFmt(this.dt[1], 'yyyy-MM-dd');
      console.log('this search params', this.search);
      // TODO调用接口
      this.content = [
        {
          jid: '1',
          description: '动转静提测',
          status: 'success',
          create_time: '2022-10-26 19:00:35',
          update_time: '2022-10-26 19:30:35'
        }
      ];
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
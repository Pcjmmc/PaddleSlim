<template>
  <div class="center-card-s">
    <div>
      <div style="margin-top: 2%;">
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
                  <p style="font-size:14px;"> {{ item.desc }}</p>
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
                  <p style="font-size:14px;"> {{ item.desc }}</p>
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
        <div>
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
            class="btn-success"
            shape="circle"
            icon="ios-search"
            @click="searchByfilter"
          >Search</Button>
        </div>
        <div style="text-align:right;">
          <span>
            <Button
              icon="md-add"
              class="btn-success"
              @click="createNewJob"
            >新建测试任务</Button>
          </span>
          <span>
            <Button
              class="btn-success"
              @click="deleteJob"
            >删除</Button>
          </span>
        </div>
      </div>
      <div style="margin-top: 1%;">
        <div class="left">
          <Table
            :columns="columns"
            :data="content"
            @on-select="addSelected"
            @on-row-click="openDrawer"
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
    </div>
    <Drawer
      :closable="true"
      width="72%"
      scrollable
      :mask-closable="false"
      v-model="showRightModa"
      v-if="selectedRow"
    >
      <div slot="header">
        <Row style="font-size:16px;">
          <Col>
            <div style="width:50px;">
              <a href="javascript:void(0)" @click="handleDetail">
                [{{ selectedRow.id }}]
              </a>
            </div>
          </Col>
          <Col>
            <div style="width:30px;">
              <Tooltip content="复制链接" placement="bottom">
                <Icon
                  class="copyBtn"
                  type="ios-link"
                  @click="copyData"
                ></Icon>
              </Tooltip>
            </div>
          </Col>
            <h3>{{ selectedRow.description }}</h3>
          <Col>
          </Col>
        </Row>
      </div>
      <div>
        <single-detail ref="mychild" :jid="selectedRow.id"></single-detail>
      </div>
    </Drawer>
    <Modal
      v-model="showModa"
      title="创建测试任务"
      width="70%"
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
import Clipboard from 'clipboard';
import { FrameWorkJobListUrl, FrameWorkDelJobUrl } from '../../api/url.js';
import TestJob from './TestJob.vue';
import SingleDetail from './SingleDetail.vue';

export default {
  name: 'CompileService',
  data: function () {
    return {
      showModa: false,
      showRightModa: false,
      tableSelect: [],
      selectedRow: null,
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
          type: 'selection',
          width: 60,
          align: 'center'
        },
        {
          title: '任务ID',
          key: 'id',
          align: 'center',
          minWidth: 60
        },
        {
          title: '任务名',
          key: 'description',
          align: 'center',
          minWidth: 300
        },
        {
          title: '任务状态',
          key: 'status',
          align: 'center',
          minWidth: 100,
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
          align: 'center',
          minWidth: 200
        },
        {
          title: '更新时间',
          key: 'update_time',
          align: 'center',
          minWidth: 200
        }
        // {
        //   title: '详情',
        //   key: 'detail',
        //   align: 'center',
        //   fixed: 'right',
        //   minWidth: 120,
        //   render: (h, params) => {
        //     return h('div', [
        //       h('Button', {
        //         props: {
        //           type: 'info'
        //         },
        //         style: {
        //           marginRight: '5px'
        //         },
        //         on: {
        //           click: () => {
        //             this.handleDetail(params.row);
        //           }
        //         }
        //       }, '查看详情')
        //     ]);
        //   }
        // }
      ],
      dt: [this.getBeginData(), new Date()],
      search: {
        name: '',
        id: null,
        status: 'all',
        begin_time: null,
        end_time: null,
        page: 1,
        pagesize: 15
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
    TestJob,
    SingleDetail
  },
  computed: {
  },
  methods: {
    getBeginData() {
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let begin_time = new Date();
      begin_time = begin_time.setDate(begin_time.getDate() - 7);
      begin_time = new Date(begin_time);
      return begin_time;
    },
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
    handleDetail() {
      let _params = {
        jid: this.selectedRow.id
      };
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'SingleDetail', params: _params});
      window.open(href, '_blank');
    },
    copyData() {
      let localHost = window.location.host;
      let url = 'http://' + localHost + '#/paddle/test/SingleDetail/410';
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
      this.tableSelect = [];
      this.content = [];
      this.search = {
        name: '',
        id: null,
        begin_time: null,
        end_time: null,
        status: 'all',
        page: 1,
        pagesize: 15
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
      // console.log('return jid is', jid);
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
    },
    addSelected(selection, row) {
      // 管理选中的选项
      console.log('select row is', row);
      this.tableSelect = selection;
      console.log('select selection is', selection);
    },
    cancelJob() {
      // 取消选中的任务
      console.log('取消选中的任务');
    },
    refreshJob() {
      // 刷新选中的任务
      console.log('刷新选中的任务');
    },
    openDrawer(row, index) {
      this.selectedRow = {};
      this.selectedRow = row;
      this.showRightModa = true;
      // 主动调用子组件的方法刷新数据
      this.$nextTick(function () {
        this.$refs.mychild.getInitData();
      });
    },
    async deleteJob() {
      // 根据选项删除
      if (this.tableSelect.length == 0) {
        this.$Message.info({
          content: '请至少勾选一个选项！',
          duration: 5,
          closable: true
        });
        return;
      }
      let count = 0;
      let len = this.tableSelect.length;
      for (let i = 0; i < this.tableSelect.length; i++) {
        let temp = this.tableSelect[i];
        let params = {
          id: temp.id
        };
        const {code, message} = await api.post(FrameWorkDelJobUrl, params);
        if (parseInt(code, 10) === 200) {
          // 从content中将index删除 todo
          count++;
          this.content.forEach((item, index) => {
            if (temp.id === item.id) {
              this.content.splice(index, 1);
            }
          })
        } else {
          this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
          });
        }
      }
      if (count === len) {
        this.$Message.info({
          content: '删除成功！',
          duration: 3,
          closable: true
        });
      }
      this.tableSelect = [];
    }
  }
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
  color:lightslategrey
}
.item-css {
  font-size: 14px;
  color: #303133;
  padding: 0 6px;
  cursor: pointer;
  -webkit-transition: border-color .3s,background-color .3s,color .3s;
  -o-transition: border-color .3s,background-color .3s,color .3s;
  transition: border-color .3s,background-color .3s,color .3s;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
}
</style>

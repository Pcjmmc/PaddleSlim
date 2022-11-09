<template>
  <div>
    <Card class="center-card-s">
      <div>
        <Form
          ref="addForm"
          :model="search"
          :label-width="75"
          style="width: 85%"
        >
          <Row>
            <Col span="12">
              <FormItem label="时间:" prop="dt">
                <DatePicker
                  type="daterange"
                  placement="bottom-end"
                  placeholder=" 开始时间 ～ 结束时间 "
                  v-model="search.dt"
                  style="width:80%"
                  v-on:on-change="searchByfilter"
                ></DatePicker>
              </FormItem>
            </Col>
          </Row>
          <div style="margin-top: 1%;">
            <Row>
              <Col span="6">
                <FormItem label="IcafeID:" prop="icafeid">
                  <Input v-model="search.icafeid" placeholder="输入icafeID"/>
                </FormItem>
              </Col>
              <Col span="6" v-if="userInfo.departmentName=='TPG质量效能部'">
                <FormItem label="RD:" prop="rdname">
                  <Input v-model="search.rdname" placeholder="输入RD邮箱前缀"/>
                </FormItem>
              </Col>
              <Col span="6" v-else>
                <FormItem label="QA:" prop="qaname">
                  <Input v-model="search.qaname" placeholder="输入QA邮箱前缀"/>
                </FormItem>
              </Col>
              <Col span="4">
                <FormItem label="状态:" prop="staus">
                  <Select clearable v-model="search.status">
                    <Option
                      :key="index"
                      :value="item"
                      v-for="(item, index) in statusList"
                    >{{ item }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="2" offset="1">
                <Button
                  type="primary"
                  shape="circle"
                  icon="ios-search"
                  @click="searchByfilter"
                >Search</Button>
              </Col>
            </Row>
          </div>
        </Form>
      </div>
      <div>
        <div style="text-align: right;">
          <Button
            icon="md-add"
            type="primary"
            @click="showCreateModa"
          >创建需求</Button>
        </div>
        <div style="margin-top: 1%;">
          <Table
            border
            :columns="columns"
            :data="content"
            width="100%"
          ></Table>
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
    <Modal
      v-model="createTestModa"
      title="提测"
      width="40%"
      v-on:on-cancel="handleResetTest"
    >
      <Form
        ref="reqDetail"
        :model="reqDetail"
        :label-width="75"
        style="width: 90%"
      >
        <FormItem label="icafeID:" prop="rd">
          <Input
            disabled
            v-model="reqDetail.icafe_id"
            placeholder="icafeId"
          />
        </FormItem>
        <FormItem label="RD:" prop="rd">
          <Input
            disabled
            v-model="reqDetail.rd"
            placeholder="提测RD邮箱前缀"
          />
        </FormItem>
        <FormItem label="QA:" prop="qa">
          <Input v-model="reqDetail.qa" placeholder="输入QA邮箱前缀"/>
        </FormItem>
        <FormItem label="repo:" prop="repo">
          <Input v-model="reqDetail.repo" placeholder="输入repo名"/>
        </FormItem>
        <FormItem label="分支:" prop="branch">
          <Input v-model="reqDetail.branch" placeholder="输入分支"/>
        </FormItem>
        <FormItem label="pr:" prop="pr">
          <Input v-model="reqDetail.pr" placeholder="输入pr号"/>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="handleResetTest">取消</Button>
        <Button type="primary" @click="handleCreateTest">提交</Button>
      </div>
    </Modal>
    <Modal
      v-model="createReqModa"
      title="创建需求"
      width="40%"
      v-on:on-cancel="handleResetReq"
    >
      <Form
        ref="addReqForm"
        :model="addReqForm"
        :label-width="75"
        :rules="addRules"
        style="width: 90%"
      >
        <FormItem label="标题:" prop="title">
          <Input v-model="addReqForm.title" placeholder="输入需求标题"/>
        </FormItem>
        <FormItem label="详情:" prop="detail">
          <Input
            clearable
            v-model="addReqForm.detail"
            type="textarea"
            placeholder="描述风险"
            :autosize="{minRows: 2,maxRows: 30}"
          />
        </FormItem>
        <FormItem label="QA:" prop="qa_owner">
          <Input v-model="addReqForm.qa_owner" placeholder="输入RD负责人邮箱前缀"/>
        </FormItem>
        <FormItem label="RD:" prop="rd_owner">
          <Input v-model="addReqForm.rd_owner" placeholder="输入QA负责人邮箱前缀"/>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="handleResetReq">取消</Button>
        <Button type="primary" @click="handleCreateReq">提交</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
// import Cookies from 'js-cookie';
import { dateFmt } from '../../util/help.js';
import { RequirementSearchUrl, UserInfoUrl, StartTestUrl, CreateReqUrl } from '../../api/url.js';
import api from '../../api/index';
import TestJob from '../PTS/TestJob.vue';

export default {
  name: 'Personal',
  data: function () {
    return {
      addReqForm: {
        rd_owner: '',
        qa_owner: '',
        title: '',
        detail: ''
      },
      addRules: {
        title: [
          { required: true, message: '请输入需求标题', trigger: 'blur' }
        ],
        qa_owner: [
          { required: true, message: '请输入QA负责人', trigger: 'blur' }
        ],
        rd_owner: [
          { required: true, message: '请输入RD负责人', trigger: 'blur' }
        ]
      },
      reqDetail: {
        rd: '',
        qa: '',
        pr: '',
        branch: '',
        repo: '',
        icafe_id: ''
      },
      createTestModa: false,
      createReqModa: false,
      selectRow: null,
      showModa: false,
      total: 0,
      page: 1,
      pagesize: 10,
      userInfo: {
      },
      statusList: [
        '待提测',
        '待测试',
        '测试中',
        '待确认',
        '测试完成'
      ],
      content: [
      ],
      search: {
        icafeid: '',
        qaname: '',
        rdname: '',
        status: '',
        dt: [this.getBeginData(), new Date()]
      },
      columns: [
        {
          title: 'IcafeID',
          key: 'sequence',
          align: 'center',
          fixed: 'left'
        },
        {
          title: '需求描述',
          key: 'title',
          align: 'center'
        },
        {
          title: '创建人',
          key: 'id',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
              }, params.row.createdUser.name)
            ]);
          }
        },
        {
          title: 'RD',
          key: 'rd_owner',
          align: 'center'
        },
        {
          title: 'QA',
          key: 'qa_owner',
          align: 'center'
        },
        {
          title: '操作',
          key: 'operation',
          align: 'center',
          fixed: 'right',
          width: '150px',
          render: (h, params) => {
            let ret = [];
            if (this.userInfo.departmentName === 'TPG质量效能部') {
              // 如果是QA，则推入操作
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.createTestJob(params.row);
                      }
                    }
                  },
                  '测试'
                )
              );
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.confirmResult(params.row);
                      }
                    }
                  },
                  '确认'
                )
              );
            } else {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.setTestModa(params.row);
                      }
                    }
                  },
                  '提测'
                )
              );
            }
            if (params.row.status === '测试完成') {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.getDetail(params.row);
                      }
                    }
                  },
                  '结果'
                )
              );
            }
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
      ]
    };
  },
  watch: {
  },
  mounted: async function () {
    this.initData();
    await this.getUserInfo();
    await this.getData();
  },
  components: {
    TestJob
  },
  computed: {
  },
  methods: {
    async handleReset() {
      await this.$refs.child.initData();
    },
    async handleSubmit() {
      await this.$refs.child.handleSubmit();
    },
    async SubmitRequirement(jid) {
      // 子组件调用将jid返给父组件，同事父组件，将icafeid和jid通过接口传递给后端
      let params = {
        test_id: jid,
        icafe_id: this.selectRow.sequence
      };
      console.log('params is, 更新需求信息，将jid写进去 todo', params);
    },
    closeModal(params) {
      // 关闭弹窗
      this.showModa = params;
    },
    getBeginData() {
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let begin_time = new Date();
      begin_time = begin_time.setDate(begin_time.getDate() - 14);
      begin_time = new Date(begin_time);
      return begin_time;
    },
    async getUserInfo() {
      const { code, data, message } = await api.get(UserInfoUrl);
      if (parseInt(code, 10) === 200) {
        this.userInfo = data;
        this.search.status = this.userInfo.departmentName === 'TPG质量效能部' ? '待测试' : '待提测';// rd默认看见的是
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async pageChange(pageNum) {
      this.page = pageNum;
      await this.getData();
    },
    async searchByfilter() {
      this.page = 1;
      await this.getData();
    },
    async getData() {
      this.content = [];
      // 如果是是rd则rd参数是自己；如果是QA则QA选项是自己
      if (this.userInfo.departmentName === 'TPG质量效能部') {
        this.search.qaname = this.userInfo.username;
      } else {
        this.search.rdname = this.userInfo.username;
      }
      let params = {
        rd: this.search.rdname,
        qa: this.search.qaname,
        page: this.page,
        status: this.search.status,
        page_num: this.pagesize,
        begin_time: dateFmt(this.search.dt[0], 'yyyy-MM-dd'),
        end_time: dateFmt(this.search.dt[1], 'yyyy-MM-dd')
      };
      const {code, data, message, all_count} = await api.get(RequirementSearchUrl, params);
      if (parseInt(code, 10) === 200) {
        this.total = all_count;
        this.content = data;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    initData() {
      this.selectRow = null;
      this.search = {
        icafeid: '',
        qaname: '',
        rdname: '',
        status: '',
        dt: [this.getBeginData(), new Date()]
      };
      this.initReqData();
      this.initTestData();
    },
    async getDetail(item) {
      // 如果改icafe已经在测试中，则可以根据绑定的jid来查看任务详情
      console.log('根据需求查看，如果已经提测');
    },
    async createTestJob(item) {
      this.selectRow = item;
      this.showModa = true;
    },
    async confirmResult(item) {
      // QA 将测试结果分发成测试成功和失败详情
      console.log('认为确认测试结果');
    },
    // 创建需求相关接口
    async handleCreateReq() {
      this.$refs.addReqForm.validate(async (valid) => {
        if (valid) {
          await this.createJob();
          await this.searchByfilter();
        } else {
          this.$Message.error('请完善信息!');
        }
      });
    },
    initReqData() {
      this.createReqModa = false;
      this.addReqForm = {
        rd_owner: '',
        qa_owner: '',
        title: '',
        detail: ''
      };
    },
    handleResetReq() {
      this.initReqData();
    },
    async showCreateModa() {
      // 将弹窗打开
      this.initReqData();
      this.createReqModa = true;
    },
    async createJob() {
      // 创建需求的API
      console.log('创建需求', this.addReqForm);
      const { code, message } = await api.post(CreateReqUrl, this.addReqForm);
      if (parseInt(code, 10) === 200) {
        this.initReqData();
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
        this.initReqData();
      }
    },
    // 提测相关操作
    setTestModa(item) {
      this.initTestData();
      this.selectRow = item;
      this.reqDetail.rd = this.userInfo.username;
      this.reqDetail.icafe_id = item.sequence;
      this.createTestModa = true;
    },
    initTestData() {
      this.createTestModa = false;
      this.selectRow = null;
      this.reqDetail = {
        rd: '',
        qa: '',
        pr: '',
        branch: '',
        repo: '',
        icafe_id: ''
      };
    },
    handleResetTest() {
      this.initTestData();
    },
    async handleCreateTest() {
      console.log('提测，', this.reqDetail);
      const { code, message } = await api.post(StartTestUrl, this.reqDetail);
      if (parseInt(code, 10) === 200) {
        this.initTestData();
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
        this.initTestData();
      }
    }
  }
};
</script>

<style scoped>
.demo-split{
  height: 861px;
  overflow:auto;
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
  max-height: 600px;
  overflow: auto;
  font-size: 15px;
  color: lightslategrey
}
.card-s-new {
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  font-size: 15px;
  color: lightslategrey
}
.ivu-form-item{
  margin-bottom: 12px;
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
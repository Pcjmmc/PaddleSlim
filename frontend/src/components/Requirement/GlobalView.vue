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
                <FormItem label="需求:" prop="keyword">
                  <Input v-model="search.keyword" placeholder="输入需求关键字"/>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="RD:" prop="rdname">
                  <Input v-model="search.rdname" placeholder="输入RD邮箱前缀"/>
                </FormItem>
              </Col>
              <Col span="6">
                <FormItem label="QA:" prop="qaname">
                  <Input v-model="search.qaname" placeholder="输入QA邮箱前缀"/>
                </FormItem>
              </Col>
              <Col span="4">
                <FormItem label="状态:" prop="staus">
                  <Select
                    clearable
                    filterable
                    v-model="search.status"
                    v-on:on-change="searchByfilter"
                  >
                    <Option
                      :key="index"
                      :value="item"
                      v-for="(item, index) in statusList"
                    >{{ item }}</Option>
                  </Select>
                </FormItem>
              </Col>
              <Col span="1" offset="1">
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
        <FormItem label="类型:" prop="type">
          <Select
            clearable
            filterable
            v-model="addReqForm.type"
          >
            <Option
              :key="index"
              :value="item"
              v-for="(item, index) in bugType"
            >{{ item }}</Option>
          </Select>
        </FormItem>
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
import Cookies from 'js-cookie';
import { dateFmt } from '../../util/help.js';
import { RequirementSearchUrl, CreateReqUrl } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'Global',
  data: function () {
    return {
      addReqForm: {
        type: 'Task',
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
      createReqModa: false,
      total: 0,
      page: 1,
      pagesize: 10,
      bugType: [
        'Task'
      ],
      statusList: [
        '全部',
        '新建',
        '开发中',
        '开发完成',
        '测试中',
        '测试完成'
      ],
      content: [
      ],
      search: {
        keyword: '',
        qaname: '',
        rdname: '',
        status: '全部',
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
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
              }, params.row.rd_owner.name)
            ]);
          }
        },
        {
          title: 'QA',
          key: 'qa_owner',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
              }, params.row.qa_owner.name)
            ]);
          }
        },
        {
          title: '状态',
          key: 'status',
          align: 'center'
        },
        {
          title: '操作',
          key: 'operation',
          align: 'center',
          fixed: 'right',
          width: '100px',
          render: (h, params) => {
            let ret = [];
            // 每一个状态要管理好操作
            if (params.row.status === '测试中') {
              if (params.row.test_id) {
                // 如果有最新的任务创建，则可以查看具体进度
                ret.push(
                  h(
                    'Button',
                    {
                      props: {
                        type: 'primary',
                        size: 'small'
                      },
                      style: {
                        marginTop: '5px',
                        marginBottom: '5px',
                        marginRight: '5px'
                      },
                      on: {
                        click: () => {
                          this.getTestJobDetail(params.row);
                        }
                      }
                    },
                    '查看进度'
                  )
                );
              }
            } else if (params.row.status === '测试完成') {
              ret.push(
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginTop: '5px',
                      marginBottom: '5px',
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.getReqDetail(params.row);
                      }
                    }
                  },
                  '查看结果'
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
    await this.getData();
  },
  components: {
  },
  computed: {
  },
  methods: {
    getBeginData() {
      // 在end_time的基础上+1， 因为end_time代表的今天0点0分0秒的时间
      let begin_time = new Date();
      begin_time = begin_time.setDate(begin_time.getDate() - 14);
      begin_time = new Date(begin_time);
      return begin_time;
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
      let params = {
        keyword: this.search.keyword,
        page: this.page,
        rd: this.search.rdname,
        qa: this.search.qaname,
        status: this.search.status === '全部' ? null : this.search.status,
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
    async showCreateModa() {
      // 将弹窗打开
      this.initReqData();
      this.createReqModa = true;
    },
    handleResetReq() {
      this.initReqData();
    },
    async createJob() {
      // 创建需求的API
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
    initReqData() {
      this.createReqModa = false;
      this.addReqForm = {
        type: 'Task',
        rd_owner: '',
        qa_owner: '',
        title: '',
        detail: ''
      };
    },
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
    initData() {
      this.initReqData();
      this.search = {
        qaname: '',
        rdname: '',
        keyword: '',
        status: '全部',
        dt: [this.getBeginData(), new Date()]
      };
    },
    async getTestJobDetail(item) {
      // 获取最新一次任务的进度
      let _params = {
        jid: item.test_id
      };
      // 根据branch获取commit列表
      const { href } = this.$router.resolve({name: 'SingleDetail', params: _params});
      window.open(href, '_blank');
    },
    async getReqDetail(item) {
      // 获取需求的整个测试详情，包括历史记录
      console.log('根据需求查看，如果已经提测');
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
  max-height: 800px;
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
<template>
  <div>
    <Row
      type="flex"
      justify="start"
      class="all-line-row"
    >
      <Col span="3" offset="0.5">
        <Select clearable v-model="search.task_type">
          <Option
            :key="index"
            :value="item.key"
            v-for="(item, index) in taskTypeList"
          >{{ item.desc }}</Option>
        </Select>
      </Col>
      <Col span="3" offset="1">
        <Input
          clearable
          v-model="search.owner"
          placeholder="负责人"
        ></Input>
      </Col>
      <Col span="3" offset="1">
        <Input
          clearable
          v-model="search.build_type_id"
          placeholder="任务唯一id"
        ></Input>
      </Col>
      <Col span="1" offset="1">
        <Button
          icon="ios-search"
          type="primary"
          @click="searchData"
        >search</Button>
      </Col>
      <Col span="2" offset="9">
        <Button type="primary" @click="activateCreateModal()">
          新增Job
        </Button>
      </Col>
    </Row>
    <Table border
      :columns="jobsColumn"
      :data="jobsList"
    ></Table>
    <Page :total="total"
      :current="parseInt(search.page)"
      :page-size="parseInt(search.pagesize)"
      @on-change="pageChange"
      size="small"
      style="text-align: center;"
      >
    </Page>
    <Modal v-model="setCreateModal" title="录入任务" @on-cancel="handleReset" width="700px">
      <Form ref="addForm" :model="addForm" :rules="addRules" :label-width="120">
        <FormItem label="所属阶段: " prop="step">
          <Select v-model="addForm.step" >
            <Option v-for="(item, index) in stepList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="所属平台: " prop="platform">
          <Select v-model="addForm.platform" >
            <Option v-for="(item, index) in platformList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
       <FormItem label="任务类型: " prop="task_type">
          <Select v-model="addForm.task_type" v-on:on-change="resetSendType1()">
            <Option v-for="(item, index) in taskTypeList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem
          label="二级分类: "
          prop="secondary_type"
          :rules="{ required: true, type: 'array', min: 1, message: '请至少选择一个二级分类', trigger: 'change' }"
          v-if="addForm.task_type == 'frame'"
        >
          <CheckboxGroup
            v-model="addForm.secondary_type"
          >
            <Checkbox
              :key="index"
              :label="item"
              v-for="(item, index) in sendType1"
            >{{ item }}</Checkbox>
          </CheckboxGroup>
        </FormItem>
        <FormItem
          label="二级分类: "
          prop="secondary_type"
          :rules="{ required: true, message: '请选择任务类型', trigger: 'blur' }"
          v-else
        >
          <RadioGroup
            v-model="addForm.secondary_type"
          >
            <Radio
              :key="index"
              :label="item"
              v-for="(item, index) in sendType1"
            >{{ item }}</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem
          label="所属repo:"
          prop="reponame"
          v-if="addForm.task_type=='model'"
        >
          <Select v-model="addForm.reponame">
            <Option
            :key="index"
            :value="item"
            v-for="(item, index) in repoeNames"
          >
          {{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务名: " prop="tname">
          <Input v-model="addForm.tname" placeholder="与tc或者效率云一致"/>
        </FormItem>
        <FormItem label="任务别名/后缀: " prop="show_name">
          <Input v-model="addForm.show_name" placeholder="简短、概括、可读"/>
        </FormItem>
        <FormItem label="任务描述: " prop="description">
          <Input v-model="addForm.description" placeholder="请简短准确概述"/>
        </FormItem>
        <FormItem label="任务覆盖的系统: " prop="system">
          <Select
            filterable
            clearable
          v-model="addForm.system"
        >
            <Option v-for="(item, index) in systemList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务唯一id: " prop="build_type_id">
          <Input v-model="addForm.build_type_id" type="textarea" :autosize="{minRows: 2,maxRows: 20}"/>
        </FormItem>
        <FormItem
          label="任务空间（xly）: "
          prop="workspace"
          v-if="addForm.step != 'compile'"
        >
          <Input
            v-model="addForm.workspace"
            type="textarea"
            :autosize="{minRows: 2,maxRows: 20}"
          ></Input>
        </FormItem>
        <FormItem label="任务负责人: " prop="owner">
          <Input v-model="addForm.owner" />
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="handleReset">取消</Button>
        <Button type="primary" @click="handleSubmit">确定</Button>
      </div>
    </Modal>
    <Modal v-model="updateModelFlag" title="修改任务" @on-cancel="handleReset" width="700px">
      <Form :model="selectedRow" :rules="addRules" :label-width="120">
        <FormItem label="所属阶段: " prop="step">
          <Select v-model="selectedRow.step" >
            <Option v-for="(item, index) in stepList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="所属平台: " prop="platform">
          <Select v-model="selectedRow.platform" >
            <Option v-for="(item, index) in platformList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
       <FormItem label="任务类型: " prop="task_type">
          <Select v-model="selectedRow.task_type" v-on:on-change="resetSendType2()">
            <Option v-for="(item, index) in taskTypeList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem
          label="二级分类: "
          prop="secondary_type"
          :rules="{ required: true, type: 'array', min: 1, message: '请至少选择一个二级分类', trigger: 'change' }"
          v-if="selectedRow.task_type == 'frame'"
        >
          <CheckboxGroup
            v-model="selectedRow.secondary_type"
          >
            <Checkbox
              :key="index"
              :label="item"
              v-for="(item, index) in sendType2"
            >{{ item }}</Checkbox>
          </CheckboxGroup>
        </FormItem>
        <FormItem
          label="二级分类: "
          prop="secondary_type"
          :rules="{ required: true, message: '请选择任务类型', trigger: 'blur' }"
          v-else
        >
          <RadioGroup
            v-model="selectedRow.secondary_type"
          >
            <Radio
              :key="index"
              :label="item"
              v-for="(item, index) in sendType2"
            >{{ item }}</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem
          label="所属repo:"
          prop="reponame"
          v-if="selectedRow.task_type=='model'"
        >
          <Select v-model="selectedRow.reponame">
            <Option
            :key="index"
            :value="item"
            v-for="(item, index) in repoeNames"
          >
          {{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务名: " prop="tname">
          <Input v-model="selectedRow.tname" placeholder="与tc或者效率云一致"/>
        </FormItem>
        <FormItem label="任务别名/后缀: " prop="show_name">
          <Input v-model="selectedRow.show_name" placeholder="简短、概括、可读"/>
        </FormItem>
        <FormItem label="任务描述: " prop="description">
          <Input v-model="selectedRow.description" placeholder="请简短准确概述"/>
        </FormItem>
        <FormItem label="任务覆盖的系统: " prop="system">
          <Select
            filterable
            clearable
            v-model="selectedRow.system"
          >
            <Option v-for="(item, index) in systemList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务唯一id: " prop="build_type_id">
          <Input v-model="selectedRow.build_type_id" type="textarea" :autosize="{minRows: 2,maxRows: 20}" disabled/>
        </FormItem>
        <FormItem label="任务空间（xly）: " prop="workspace">
          <Input
          v-model="selectedRow.workspace"
          type="textarea"
          :autosize="{minRows: 2,maxRows: 20}"
          ></Input>
        </FormItem>
        <FormItem label="任务负责人: " prop="owner">
          <Input v-model="selectedRow.owner" />
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="handleReset">取消</Button>
        <Button type="primary" @click="handelUpdateSubmit">确定</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
import Cookies from 'js-cookie';
import api from '../../api/index';
import { ScenesUrl, JobUrl } from '../../api/url.js';
export default {
  name: 'JobsManage',
  props: {},
  data: function () {
    return {
      selectedRow: {},
      jobsList: [],
      total: 0,
      setCreateModal: false,
      updateModelFlag: false,
      search: {
        owner: '',
        build_type_id: '',
        task_type: '',
        page: 1,
        pagesize: 10
      },
      platformList: [
        {
          'key': 'xly',
          'desc': '效率云'
        },
        {
          'key': 'teamcity',
          'desc': 'teamcity'
        }
      ],
      taskTypeList: [
      ],
      sendTypeList: {},
      sendType2: [],
      sendType1: [],
      repoeNames: [
        'other',
        'PaddleClas',
        'PaddleGAN',
        'PaddleOCR',
        'PaddleNLP',
        'PaddleSeg',
        'PaddleDetection',
        'PaddleSpeech',
        'PaddleRec',
        'PaddleSlim',
        'PaddleHub',
        'Paddle2ONNX',
        'PaddleScience',
        'MultipleRepos',
        'CINN'
      ],
      systemList: [],
      stepList: [
        // {
        //   'key': 'compile',
        //   'desc': '编译'
        // },
        {
          'key': 'develop',
          'desc': 'dev回归'
        },
        {
          'key': 'release',
          'desc': '发版回归'
        },
        {
          'key': 'shared',
          'desc': 'dev/发版'
        }
      ],
      addForm: {
        'tname': '',
        'owner': '',
        'build_type_id': '',
        'platform': '',
        'system': '',
        'task_type': '',
        'secondary_type': null,
        'workspace': '',
        'description': '',
        'step': '',
        'reponame': '',
        'show_name': ''
      },
      addRules: {
        step: [
          { required: true, message: '请选择任务阶段', trigger: 'blur' }
        ],
        tname: [
          { required: true, message: '请输入任务名', trigger: 'blur' }
        ],
        owner: [
          { required: true, message: '请输入负责人', trigger: 'blur' }
        ],
        build_type_id: [
          { required: true, message: '请选择任务唯一id', trigger: 'blur' }
        ],
        platform: [
          { required: true, message: '请选择任务所在平台', trigger: 'blur' }
        ],
        system: [
          { required: true, message: '请选择任务覆盖系统', trigger: 'blur' }
        ],
        task_type: [
          { required: true, message: '请选择任务类型', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请填写任务描述', trigger: 'blur' }
        ]
      },
      jobsColumn: [
        {
          title: '任务名',
          key: 'tname',
          fixed: 'left'
        },
        {
          title: '阶段',
          key: 'step'
        },
        {
          title: '覆盖平台',
          key: 'system',
          width: '120',
          filters: [
          ],
          filterMultiple: false,
          filterMethod(value, row) {
            return row.system === value;
          }
        },
        {
          title: '任务描述',
          key: 'description'
        },
        {
          title: '任务别名/后缀',
          key: 'show_name'
        },
        {
          title: '任务所在平台',
          key: 'platform'
        },
        {
          title: '任务类型',
          key: 'task_type',
          render: (h, params) => {
            return h('span', {
            }, this.getDescBykey(params.row.task_type));
          }
        },
        {
          title: '二级分类',
          key: 'secondary_type',
          render: (h, params) => {
            return h('span', {
            }, this.getDesc(params.row.secondary_type));
          }
        },
        {
          title: '负责人',
          key: 'owner'
        },
        {
          title: '唯一id',
          key: 'build_type_id'
        },
        {
          title: '任务空间',
          key: 'workspace'
        },
        {
          title: '操作',
          align: 'center',
          width: 150,
          fixed: 'right',
          render: (h, params) => {
            let ret = []
            ret.push(
              h(
                'Button',
                {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.handleDel(params.row)
                    }
                  }
                },
                '删除'
              )
            )
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
                      this.handelUpdate(params.row)
                    }
                  }
                },
                '修改'
              )
            )
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
            )
          }
        }
      ]
    };
  },
  watch: {
  },
  mounted: function () {
    this.getJobData();
  },
  components: {
  },
  methods: {
    async getJobData() {
      this.initData();
      await this.getScenesList();
      let params = {
        page: this.search.page,
        pagesize: this.search.pagesize,
        owner: this.search.owner,
        task_type: this.search.task_type,
        build_type_id: this.search.build_type_id,
        appid: Cookies.get('appid')
      };
      const {code, all_count, data, msg} = await api.get(JobUrl, params);
      if (parseInt(code) == 200) {
        this.total = all_count;
        this.jobsList = data;
        this.getStatusFilters();
      } else {
        this.total = 0;
        this.jobsList = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        })
      }
    },
    initData() {
      this.setCreateModal = false;
      this.$refs['addForm'].resetFields();
      this.updateModelFlag = false;
      this.selectedRow = {};
    },
    activateCreateModal() {
      this.setCreateModal = true;
    },
    handleReset(auto) {
      this.initData();
    },
    async handleDel(row) {
      let params = {
        id: row.id
      }
      const {code, msg} = await api.delete(JobUrl, params);
      if (parseInt(code) != 200) {
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        })
      }
      this.getJobData();
    },
    handelUpdate(row) {
      this.selectedRow = row;
      this.updateModelFlag = true;
      this.sendType2 = this.sendTypeList[row.task_type];
    },
    async handelUpdateSubmit() {
      let params = {
        id: this.selectedRow.id,
        build_type_id: this.selectedRow.build_type_id,
        workspace: this.selectedRow.workspace,
        description: this.selectedRow.description,
        owner: this.selectedRow.owner,
        platform: this.selectedRow.platform,
        step: this.selectedRow.step,
        system: this.selectedRow.system,
        task_type: this.selectedRow.task_type,
        secondary_type: this.selectedRow.secondary_type,
        tname: this.selectedRow.tname,
        reponame: this.selectedRow.reponame,
        show_name: this.selectedRow.show_name,
        appid: Cookies.get('appid')
      }
      if (params.secondary_type instanceof Array) {
        let tmp = params.secondary_type.filter(v => this.sendType2.includes(v));
        params.secondary_type = tmp.join(',');
      }
      // 将数组用都好分割拼接
      // console.log('up data job params is', this.selectedRow.secondary_type);
      const {code, msg} = await api.put(JobUrl, params);
      if (parseInt(code) != 200) {
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        })
      }
      this.getJobData();
    },
    handleSubmit() {
      this.$refs['addForm'].validate((valid) => {
        if (valid) {
          this.createJob();
        } else {
          this.$Message.error('请完善job信息');
        }
      })
    },
    async createJob() {
      let params = {
        appid: Cookies.get('appid')
      };
      params = Object.assign(params, this.addForm);
      if (params.secondary_type instanceof Array) {
        params.secondary_type = params.secondary_type.join(',');
      }
      const {code, msg} = await api.post(JobUrl, params);
      this.initData();
    },
    resetSendType1() {
      this.sendType1 = this.sendTypeList[this.addForm.task_type];
      // console.log('sendType1 is', this.sendType1);
    },
    resetSendType2() {
      this.sendType2 = this.sendTypeList[this.selectedRow.task_type];
    },
    async getScenesList() {
      const {code, data, msg} = await api.get(ScenesUrl);
      if (parseInt(code) == 200) {
        this.taskTypeList = data.taskTypeList;
        this.sendTypeList = data.sendTypeList;
        this.systemList = data.systemList;
      } else {
        this.taskTypeList = []
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        })
      }
    },
    searchData() {
      this.search.page = 1;
      this.getJobData();
    },
    getDescBykey(key) {
      for (let idx in this.taskTypeList) {
        if (this.taskTypeList[idx].key === key) {
          return this.taskTypeList[idx].desc;
        }
      }
      return '未知';
    },
    getDesc(secondary_type) {
      if (secondary_type instanceof Array) {
        return secondary_type.join(',');
      }
      return secondary_type;
    },
    pageChange(pageNum) {
      this.search.page = pageNum;
      this.getJobData();
    },
    getStatusFilters() {
      let filterst = [];
      let filters = [];
      for (var i = 0; i < this.jobsList.length; i++) {
        let system = this.jobsList[i].system;
        filterst.push(system);
      }
      this.newfilterst = Array.from(new Set(filterst));
      for (var j = 0; j < this.newfilterst.length; j++) {
        filters[j] = {
          label: this.newfilterst[j],
          value: this.newfilterst[j]
        };
      }
      this.jobsColumn[2].filters = filters;
    }
  }
};
</script>
<style scoped>
.all-line-row {
  margin-bottom: 1%;
  margin-top: 1%;
}
</style>
<template>
  <div>
    <Row
      type="flex"
      justify="end"
      style="margin-bottom: 1%;margin-top: 2%"
    >
      <col>
        <Button type="primary" @click="activateCreateModal()">
          新增Job
        </Button>
      </col>
    </Row>
    <Table border
      :columns="jobsColumn"
      :data="jobsList"
    ></Table>
    <Page :total="total"
      :current="parseInt(search.page)"
      :page-size="parseInt(search.pagesize)"
      @on-change="PageChange()"
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
        <FormItem label="二级分类: " prop="secondary_type">
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
        <FormItem label="任务描述: " prop="description">
          <Input v-model="addForm.description" placeholder="请简短准确概述"/>
        </FormItem>
        <FormItem label="任务覆盖的系统: " prop="system">
          <Select v-model="addForm.system" >
            <Option v-for="(item, index) in systemList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务唯一id: " prop="build_type_id">
          <Input v-model="addForm.build_type_id" type="textarea" :autosize="{minRows: 2,maxRows: 20}"/>
        </FormItem>
        <FormItem label="依赖任务唯一id: " prop="dependencies" v-if="addForm.step != 'compile'">
          <Input v-model="addForm.dependencies" type="textarea" :autosize="{minRows: 2,maxRows: 20}"/>
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
        <FormItem label="二级分类: " prop="secondary_type">
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
        <FormItem label="任务描述: " prop="description">
          <Input v-model="selectedRow.description" placeholder="请简短准确概述"/>
        </FormItem>
        <FormItem label="任务覆盖的系统: " prop="system">
          <Select v-model="selectedRow.system" >
            <Option v-for="(item, index) in systemList" :value="item.key" :key="index">{{ item.desc }}</Option>
          </Select>
        </FormItem>
        <FormItem label="任务唯一id: " prop="build_type_id">
          <Input v-model="selectedRow.build_type_id" type="textarea" :autosize="{minRows: 2,maxRows: 20}" disabled/>
        </FormItem>
        <FormItem label="依赖任务唯一id: " prop="dependencies">
          <Input v-model="selectedRow.dependencies" type="textarea" :autosize="{minRows: 2,maxRows: 20}"/>
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
        page: 1,
        pagesize: 20
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
        'PaddleGan',
        'PaddleOCR',
        'PaddleNLP',
        'PaddleSeg',
        'PaddleDetection',
        'PaddleSpeech',
        'PaddleRec',
        'PaddleSlim',
        'PaddleHub'
      ],
      systemList: [
        {
          'key': 'Linux_Gpu_Cuda10.1',
          'desc': 'Linux_Gpu_Cuda10.1'
        },
        {
          'key': 'Linux_Gpu_Cuda10.2',
          'desc': 'Linux_Gpu_Cuda10.2'
        },
        {
          'key': 'Linux_Gpu_Cuda11.0',
          'desc': 'Linux_Gpu_Cuda11.0'
        },
        {
          'key': 'Linux_Gpu_Cuda11.1',
          'desc': 'Linux_Gpu_Cuda11.1'
        },
        {
          'key': 'Linux_Gpu_Cuda11.2',
          'desc': 'Linux_Gpu_Cuda11.2'
        },
        {
          'key': 'Linux_Gpu(T4)_Cuda10.2',
          'desc': 'Linux_Gpu(T4)_Cuda10.2'
        },
        {
          'key': 'Linux_Gpu(T4)_Cuda11.2',
          'desc': 'Linux_Gpu(T4)_Cuda11.2'
        },
        {
          'key': 'Linux_Gpu_Cuda11.2',
          'desc': 'Linux_Gpu_Cuda11.2'
        },
        {
          'key': 'Linux_Cpu',
          'desc': 'Linux_Cpu'
        },
        {
          'key': 'Mac',
          'desc': 'Mac'
        },
        {
          'key': 'Windows_GPU_3080',
          'desc': 'Windows_GPU_3080'
        },
        {
          'key': 'Windows_GPU_2080',
          'desc': 'Windows_GPU_2080'
        },
        {
          'key': 'Windows_Cpu',
          'desc': 'Windows_Cpu'
        },
        {
          'key': 'Xpu',
          'desc': 'Xpu'
        },
        {
          'key': 'Linux-Jetpack',
          'desc': 'Linux-Jetpack'
        }
      ],
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
        'secondary_type': [],
        'dependencies': '',
        'description': '',
        'step': '',
        'reponame': ''
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
        secondary_type: [
          { required: true, type: 'array', min: 1, message: '请至少选择一个二级分类', trigger: 'change' }
          // { required: true, message: '请选择任务类型', trigger: 'blur' }
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
          key: 'system'
        },
        {
          title: '任务描述',
          key: 'description'
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
          key: 'secondary_type'
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
          title: '任务依赖',
          key: 'dependencies'
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
        appid: Cookies.get('appid')
      };
      const {code, all_count, data, msg} = await api.get(JobUrl, params);
      if (parseInt(code) == 200) {
        this.total = all_count;
        this.jobsList = data;
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
        dependencies: this.selectedRow.dependencies,
        description: this.selectedRow.description,
        owner: this.selectedRow.owner,
        step: this.selectedRow.step,
        system: this.selectedRow.system,
        task_type: this.selectedRow.task_type,
        secondary_type: JSON.stringify(this.selectedRow.secondary_type),
        // secondary_type: this.selectedRow.secondary_type,
        tname: this.selectedRow.tname,
        reponame: this.selectedRow.reponame,
        appid: Cookies.get('appid')
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
      params.secondary_type = JSON.stringify(params.secondary_type);
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
      } else {
        this.taskTypeList = []
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        })
      }
    },
    getDescBykey(key) {
      for (let idx in this.taskTypeList) {
        if (this.taskTypeList[idx].key === key) {
          return this.taskTypeList[idx].desc;
        }
      }
      return '未知';
    },
    pageChange(pageNum) {
      this.search.page = pageNum;
      this.getJobData();
    }
  }
};
</script>
<style scoped>
</style>
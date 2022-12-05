<template>
  <div class="all-line-row">
    <Row
      type="flex"
      justify="end"
    >
      <div v-if="jobsList.length > 0">
        <Button disabled>
          <p style="font-size:14px;">开启release监控</p>
        </Button>
      </div>
      <div v-else>
        <Button type="primary" @click="activateCreateModal()">
          <p style="font-size:14px;">开启release监控</p>
        </Button>
      </div>
    </Row>
    <p style="font-size:14px;">计划中的版本</p>
    <Table
      border
      :columns="jobsColumn"
      :data="jobsList"
    ></Table>
    <Modal
      v-model="setCreateModal"
      title="创建发版计划"
      width="700px"
      v-on:on-cancel="handleReset"
    >
      <Form
        ref="addForm"
        :model="addForm"
        :rules="addRules"
        :label-width="120"
      >
        <FormItem label="分支:" prop="branch">
          <Input v-model="addForm.branch" placeholder="输入分支"/>
        </FormItem>
        <FormItem label="计划版本:" prop="tag">
         <Input v-model="addForm.tag" placeholder="输入计划的版本"/>
        </FormItem>
        <FormItem label="开始commit:" prop="begin_commit">
          <Input v-model="addForm.begin_commit" placeholder="输入开始的commit"/>
        </FormItem>
      </Form>
      <div slot="footer">
        <Button type="text" @click="handleReset">取消</Button>
        <Button type="primary" @click="handleSubmit">确定</Button>
      </div>
    </Modal>
    <Modal
      v-model="showTag"
      title="更新集测信息"
      width="700px"
      v-on:on-cancel="handleReset"
    >
      <Form :model="selectedRow" :label-width="130">
        <FormItem label="分支:" prop="branch">
          <Input
            disabled
            v-model="selectedRow.branch"
            placeholder="输入分支"
          />
        </FormItem>
        <FormItem
          label="正式tag:"
          prop="tag"
          :rules="{ required: true, message: '请输入tag名', trigger: 'blur' }"
        >
         <Input
            v-model="selectedRow.tag"
            placeholder="输入计划的版本"
        />
        </FormItem>
         <FormItem
          v-if="updateModelPlan"
          label="开始commit:"
          prop="begin_commit"
          :rules="{ required: true, message: '请输入集测开始的commit', trigger: 'blur' }"
        >
          <Input
            v-model="selectedRow.begin_commit"
            placeholder="输入开始的commit"
          />
        </FormItem>
        <FormItem
          v-if="updateModelPlan"
          label="icafe所属计划"
          prop="icafe_plan"
          :rules="{ required: true, message: '请输入icafe所属计划空间名', trigger: 'blur' }"
        >
          <Input
            v-model="selectedRow.icafe_plan"
            placeholder="请输入icafe所属计划空间名"
          />
        </FormItem>
        <FormItem
          v-if="updateModelTag"
          label="结束commit:"
          prop="end_commit"
          :rules="{ required: true, message: '请输入集测结束commit', trigger: 'blur' }"
        >
          <Input
            v-model="selectedRow.end_commit"
            placeholder="输入结束的commit"
          />
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
import api from '../../api/index';
import { dateFmt, timestampToTime } from '../../util/help.js';
import { VersionUrl } from '../../api/url.js';
export default {
  name: 'VersionManage',
  props: {},
  data: function () {
    return {
      selectedRow: {
        branch: '',
        tag: '',
        begin_commit: '',
        end_commit: '',
        icafe_plan: ''
      },
      showTag: false,
      updateModelTag: false,
      updateModelPlan: false,
      setCreateModal: false,
      addForm: {
        branch: '',
        tag: '',
        begin_commit: ''
      },
      jobsList: [],
      jobsColumn: [
        {
          title: '分支',
          key: 'branch',
          fixed: 'left'
        },
        {
          title: '正式/计划版本号',
          key: 'tag'
        },
        {
          title: '开始commit',
          width: 350,
          key: 'begin_commit'
        },
        {
          title: '创建时间',
          key: 'created',
          render: (h, params) => {
            return h('p', {
            }, this.changeTimestamp(params.row.created));
          }
        },
        {
          title: '操作',
          align: 'center',
          width: 250,
          fixed: 'right',
          render: (h, params) => {
            let ret = [];
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
                      this.handelUpdate(params.row, 'begin');
                    }
                  }
                },
                '开启集测'
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
                      this.handelUpdate(params.row, 'end');
                    }
                  }
                },
                '打tag'
              )
            );
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
                      this.handleDel(params.row);
                    }
                  }
                },
                '删除'
              )
            );
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
      addRules: {
        branch: [
          { required: true, message: '请输入分支', trigger: 'blur' }
        ],
        tag: [
          { required: true, message: '请输入发版计划名', trigger: 'blur' }
        ],
        begin_commit: [
          { required: true, message: '请输入开始的commit', trigger: 'blur' }
        ]
      }
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
      // 获取发版计划
      this.jobsList = [];
      const {code, data, message} = await api.get(VersionUrl);
      if (parseInt(code, 10) === 200) {
        this.jobsList = data;
      } else {
        this.jobsList = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    initData() {
      this.showTag = false;
      this.updateModelTag = false;
      this.updateModelPlan = false;
      this.setCreateModal = false;
      this.addForm = {
        branch: '',
        tag: '',
        begin_commit: ''
      };
      this.selectedRow = {
        branch: '',
        tag: '',
        begin_commit: '',
        end_commit: ''
      };
    },
    activateCreateModal() {
      this.setCreateModal = true;
    },
    changeTimestamp(timestamp, offset = 8) {
      if (timestamp) {
        let date = timestampToTime(timestamp, offset);
        let dt = dateFmt(date, 'yyyy-MM-dd hh:mm:ss');
        return dt;
      } else {
        return '';
      }
    },
    handelUpdate(row, step) {
      this.showTag = true;
      this.selectedRow = row;
      if (step === 'begin') {
        this.updateModelPlan = true;
      } else {
        this.updateModelTag = true;
      }
    },
    handleSubmit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.createJob();
          this.initData();
        } else {
          this.$Message.error('请完善信息');
        }
      });
    },
    async handelUpdateSubmit() {
      console.log('this selectedRow', this.selectedRow);
      const {code, message} = await api.put(VersionUrl, this.selectedRow);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
      this.initData();
      this.getJobData();
    },
    handleReset(auto) {
      this.initData();
      this.getJobData();
    },
    async handleDel(row) {
      let params = {id: row.id};
      const {code, message} = await api.delete(VersionUrl, params);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      } else {
        this.getJobData();
      }
    },
    async createJob() {
      const {code, message} = await api.post(VersionUrl, this.addForm);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      } else {
        this.getJobData();
      }
    }
  }
};
</script>
<style scoped>
.all-line-row {
  font-size: 14px;
  margin-left:1%;
  margin-top: 1%;
  margin-right:1%
}
</style>
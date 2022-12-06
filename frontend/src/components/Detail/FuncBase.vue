<template>
    <div class="all-line-row">
      <Card class="center-card-s">
        <p
          style="text-align: center;font-size:16px;"
          v-if="index==0"
        >
          <Icon type="ios-information-circle" size="20"></Icon>
          {{ "任务信息概述" }}
        </p>
        <span
          style="text-align:left;font-size: 14px;"
          v-if="index==0"
        >
          任务名: {{ $route.query.tname }}
        <span style="float:right;">
          <ButtonGroup size="small">
            <Button type="text" @click="associatedBug()">关联卡片</Button>
            <Button type="text" @click="createBug()">新建卡片</Button>
          </ButtonGroup>
        </span>
        </span>
        <p
          style="text-align: left;font-size: 14px;"
          v-if="index==0"
        >
          repo信息: {{ $route.query.repo }}
        </p>
        <p
          style="text-align: left;font-size: 14px;"
          v-if="index==0"
        >
          commit信息: {{ $route.query.commit_id }}
        </p>
        <p
          style="text-align: left;font-size: 14px;"
          v-if="index==0"
        >
          commit提交时间: {{ changeTimestamp($route.query.commit_time) }}
        </p>
        <p
          style="text-align: left;font-size: 14px;"
          v-if="index==0"
        >
          分支信息: {{ $route.query.branch }}
        </p>
        <p
          style="text-align: left;font-size: 14px;"
          v-if="index==0"
        >
          执行时间: {{ changeTimestamp($route.query.created) }}
        </p>
        <p
          style="text-align: left;font-size: 14px;color: red"
          v-if="index==0 && $route.query.status.toLowerCase()=='failed'"
        >
          执行结果: {{ $route.query.status }}
        </p>
        <p
          style="text-align: left;font-size: 14px;color: green"
          v-else-if="index==0"
        >
          执行结果: {{ $route.query.status }}
        </p>
        <p
          style="text-align: left;font-size: 14px;color: red"
          v-if="$route.query.status.toLowerCase()=='failed' && index==0"
        >
          原因: {{ getErrorReason($route.query.exit_code) }}
        </p>
      </Card>
      <Card
        class="center-card-s"
        v-if="bugList.length > 0"
      >
        <p slot="title" style="text-align: center;font-size: 16px;">
          关联卡片
        </p>
        <icafe-base :datas="bugList"></icafe-base>
      </Card>
      <Card class="center-card-s">
        <p slot="title" style="text-align: center;font-size: 16px;">
          {{ secondarytype }}
        </p>
        <Table
          border
          :columns="detailColumns"
          :data="summarydata"
        >
        </Table>
      </Card>
      <Card
        v-if="failedData.length > 0"
        class="center-card-s"
      >
        <p slot="title" style="text-align: center;font-size: 16px;">
          {{ "失败case" }}
        </p>
        <Scroll
          :height="contentHeight"
          :on-reach-bottom="addDataArr"
          :loading-text="loadingText"
        >
          <frame-detail-base
            :data="failedData"
            :columns="Columns"
          >
          </frame-detail-base>
        </Scroll>
      </Card>
      <Card
        v-if="succeedData.length > 0"
        class="center-card-s"
      >
        <p slot="title" style="text-align: center;font-size: 16px;">
          {{ "成功case" }}
        </p>
        <Scroll
          :height="contentHeight2"
          :on-reach-bottom="addDataArr"
          :loading-text="loadingText2"
        >
          <frame-detail-base
            :data="succeedData"
            :columns="Columns"
          >
          </frame-detail-base>
        </Scroll>
      </Card>
      <Modal
        v-model="ShowDetail"
        title="用例详情"
        width="1000px"
      >
        <vue-json-pretty
          :data="ErrorDetail"
        >
        </vue-json-pretty>
        <div slot="footer">
        </div>
      </Modal>
      <Modal
        v-model="creatBugTag"
        title="快速创建bug卡片"
        width="600px"
        v-on:on-cancel="handleReset"
      >
        <Form
          :model="addForm"
          :rules="addRules"
          :label-width="100"
        >
          <FormItem label="计划版本/分支: " v-if="$route.query.branch=='develop'">
            <Input v-model="$route.query.branch"/>
          </FormItem>
          <FormItem label="计划版本/分支: " v-else>
            <Input v-model="addForm.tag"/>
          </FormItem>
          <FormItem label="bug发现方式: ">
            <Input readonly v-model="addForm.bug_type"/>
          </FormItem>
          <FormItem label="repo: ">
            <Input readonly v-model="addForm.repo"/>
          </FormItem>
          <FormItem label="卡片标题: " prop="title">
            <Input v-model="addForm.title"/>
          </FormItem>
          <FormItem label="等级" prop="level">
            <Select v-model="addForm.level">
              <Option
                :key="index"
                :value="item.desc"
                v-for="(item, index) in levelList"
              >{{ item.desc }}</Option>
            </Select>
          </FormItem>
          <FormItem label="rd负责人" prop="rd_owner">
            <Input v-model="addForm.rd_owner"/>
          </FormItem>
          <FormItem label="qa负责人" prop="qa_owner">
            <Input v-model="addForm.qa_owner"/>
          </FormItem>
          <FormItem label="详情描述: " prop="description">
            <Input
              v-model="addForm.description"
              type="textarea"
              :autosize="{minRows: 2,maxRows: 20}"
            />
          </FormItem>
          <FormItem prop="upimg" label="上传">
            <div class="demo-upload-list" v-for="item in tmpList">
              <template v-if="item">
                <img :src="item.content">
                <div class="demo-upload-list-cover">
                  <Icon type="ios-eye-outline" @click.native="handleView(item)"></Icon>
                  <Icon type="ios-trash-outline" @click.native="handleRemove(item.name)"></Icon>
                </div>
              </template>
              <template v-else>
                <Progress
                  v-if="item.showProgress"
                  :percent="item.percentage"
                  hide-info
                ></Progress>
              </template>
            </div>
            <Upload
              type="drag"
              style="display: inline-block;width:58px;"
              multiple
              action="/"
              :show-upload-list="false"
              :default-file-list="defaultList"
              :format="['jpg','jpeg','png']"
              :max-size="10240"
              :before-upload="handleBeforeUpload"
              :on-format-error="handleFormatError"
              :on-exceeded-size="handleMaxSize"
            >
              <div style="width: 58px;height:58px;line-height: 58px;">
                <Button icon="ios-camera"></Button>
              </div>
            </Upload>
            <Modal title="View Image" v-model="visible">
              <img
                :src="images"
                v-if="visible"
                style="width: 100%"
              >
            </Modal>
          </FormItem>
        </Form>
        <div slot="footer">
          <Button type="text" @click="handleReset">取消</Button>
          <Button type="primary" @click="handleSubmit">确定</Button>
        </div>
      </Modal>
      <Modal
        width="600px"
        v-model="associatedBugTag"
        title="关联已有卡片"
        v-on:on-cancel="cancelAssociate"
      >
        <Form
          :model="associateForm"
          :label-width="120"
        >
          <FormItem label="计划版本/分支: " v-if="$route.query.branch=='develop'">
            <Input v-model="$route.query.branch"/>
          </FormItem>
          <FormItem label="计划版本/分支: " v-else>
            <Input v-model="associateForm.tag"/>
          </FormItem>
          <FormItem label="卡片地址: ">
            <Input v-model="associateForm.issues_url"/>
          </FormItem>
        </Form>
        <div slot="footer">
          <Button type="text" @click="cancelAssociate">取消</Button>
          <Button type="primary" @click="handleAssociate">确定</Button>
        </div>
      </Modal>
    </div>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import { dateFmt, timestampToTime } from '../../util/help.js';
import frameDetailBase from '../base/frameDetailBase.vue';
import { BugUrl, ScenesUrl, AssociateBugUrl } from '../../api/url.js';
import icafeBase from '../Base/icafeBase.vue';
import api from '../../api/index';
export default {
  props: {
    'detail': {
      type: Object,
      default: function () {
        return null;
      }
    },
    'secondarytype': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'summarydata': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    index: {
      type: [Number],
      default: function () {
        return null;
      }
    }
  },
  data: function () {
    return {
      bugList: [],
      creatBugTag: false,
      associatedBugTag: false,
      images: '',
      visible: false,
      uploadList: [],
      tmpList: [],
      defaultList: [],
      levelList: [
        {
          key: 327681,
          desc: 'P0-致命问题 Highest'
        },
        {
          key: 327682,
          desc: 'P1-严重问题 High'
        },
        {
          key: 327683,
          desc: 'P2-一般问题 Middle'
        },
        {
          key: 627460,
          desc: 'P3-个体问题 Lowest'
        }
      ],
      associateForm: {
        secondary_type: this.secondarytype,
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        tag: this.$route.query.tag,
        issues_url: ''
      },
      addForm: {
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        secondary_type: this.secondarytype,
        repo: this.$route.query.repo,
        bug_type: '',
        tag: this.$route.query.tag,
        title: '',
        description: '',
        level: 'P0-致命问题 Highest',
        qa_owner: '',
        rd_owner: ''
      },
      addRules: {
        title: [
          { required: true, message: '请输入卡片标题', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入错误详情', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择等级', trigger: 'blur' }
        ],
        qa_owner: [
          { required: true, message: '请输入rd负责人', trigger: 'blur' }
        ],
        rd_owner: [
          { required: true, message: '请输入qa负责人', trigger: 'blur' }
        ]
      },
      ShowDetail: false,
      bugTypeList: {},
      ErrorDetail: {},
      failedData: [],
      succeedData: [],
      contentHeight2: 100,
      contentHeight: 100,
      loadingText: '加载中',
      loadingText2: '加载中',
      num: 10,
      bugColumns: [
        {
          title: '所属计划',
          key: 'tag',
          align: 'center'
        },
        {
          title: '卡片地址',
          key: 'issues_url',
          align: 'center'
        }
      ],
      detailColumns: [
        {
          title: '总数',
          key: 'total',
          align: 'center'
        },
        {
          title: '失败case数',
          key: 'failed_num',
          align: 'center'
        },
        {
          title: '成功case数',
          key: 'passed_num',
          align: 'center'
        }
      ],
      Columns: [
        {
          title: '文件名',
          key: 'fullName',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('p', {
                style: {
                  marginRight: '5px'
                }
              }, params.row.fullName.split('#')[0])
            ]);
          }
        },
        {
          title: 'case名',
          key: 'name',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            const { status } = params.row;
            return h('div', [
              h('Tag', {
              props: {
                color: this.setColor(status)
              }
              }, status)
            ]);
          }
        },
        {
          title: '注释',
          minWidth: 200,
          key: 'description',
          align: 'center'
        },
        {
          title: '详情',
          key: 'statusDetails',
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'primary'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.handleEdit(params.row);
                  }
                }
              }, '详情')
            ]);
          }
        }
      ],
      ExpandColumns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            // console.log('params', params.row.data);
            return h(frameDetailBase, {
                props: {
                  data: params.row.data,
                  columns: this.Columns
                }
            });
          }
        },
        {
          title: '阶段名',
          key: 'step',
          align: 'center'
        },
        {
          title: '状态',
          key: 'status',
          align: 'center'
        }
      ]
    };
  },
  mounted: function () {
    // console.log('data', this.detail);
    this.addDataArr();
    this.initHeight();
    this.getScenesList();
    this.getBugList();
  },
  components: {
    VueJsonPretty,
    frameDetailBase,
    icafeBase
  },
  computed: {
    allSourceFailed() {
      return this.detail.failed_data;
    },
    allSourceSuccess() {
      return this.detail.succeed_data;
    }
  },
  methods: {
    getErrorReason(exit_code) {
      switch (parseInt(exit_code, 10)) {
        case 0:
          return '成功';
        case 2:
          return 'CE框架失败';
        case 3:
          return '模型yaml书写错误';
        case 4:
          return 'Lite模型优化失败';
        case 5:
          return '未录入任务';
        case 7:
          return '编译失败';
        case 8:
          return 'case失败';
        case 63:
          return '克隆代码失败';
        case 125:
          return '启动容器失败';
        case 127:
          return 'tc没有执行权限';
        case 137:
          return 'tc任务取消';
        default:
          return '未知';
      }
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
    handleEdit(row) {
      this.ShowDetail = true;
      this.ErrorDetail = row;
    },
    initHeight() {
      let max_len1 = this.failedData.length;
      if (max_len1 > 0) {
        if (max_len1 <= 5) {
          this.contentHeight = (100 - (max_len1 - 1) * 10) * max_len1;
        } else if (max_len1 < 10) {
          this.contentHeight = 80 * max_len1;
        } else {
          this.contentHeight = 500;
        }
      }
      let max_len = this.succeedData.length;
      if (max_len > 0) {
        if (max_len <= 5) {
          this.contentHeight2 = (100 - (max_len - 1) * 10) * max_len;
        } else if (max_len < 10) {
          this.contentHeight2 = 80 * max_len;
        } else {
          this.contentHeight2 = 500;
        }
      }
    },
    addDataArr() {
      let max_len1 = Object.keys(this.allSourceFailed).length;
      if (max_len1 > 0) {
        let i = 0;
        max_len1 = max_len1 > this.num ? this.num : max_len1;
        for (let vd in this.allSourceFailed) {
          if (i < max_len1 && this.allSourceFailed[vd]) {
            this.failedData.push(this.allSourceFailed[vd]);
            this.allSourceFailed[vd] = null;
            delete this.allSourceFailed[vd];
            i = i + 1;
          } else {
            break;
          }
        }
      }
      let max_len = Object.keys(this.allSourceSuccess).length;
      if (max_len > 0) {
        let j = 0;
        max_len = max_len > this.num ? this.num : max_len;
        for (let vd in this.allSourceSuccess) {
          if (j < max_len && this.allSourceSuccess[vd]) {
            this.succeedData.push(this.allSourceSuccess[vd]);
            this.allSourceSuccess[vd] = null;
            delete this.allSourceSuccess[vd];
            j = j + 1;
          } else {
            break;
          }
        }
      }
      if (max_len === 0) {
        this.loadingText2 = '加载完成';
      }
      if (max_len1 === 0) {
        this.loadingText = '加载完成';
      }
    },
    // separateData() {
    //   let succeedArray = [];
    //   let faliedArray = [];
    //   for (var idx = 0; idx < this.detail.length; idx++) {
    //     let item = this.detail[idx];
    //     if (!item.status) {
    //       continue;
    //     }
    //     if (item.status.toLowerCase() === 'broken') {
    //       item.status = 'failed';
    //     }
    //     if (item.status.toLowerCase() === 'failed') {
    //       faliedArray.push(item);
    //     } else {
    //       succeedArray.push(item);
    //     }
    //   }
    //   let result = {
    //     'succeedArray': [],
    //     'faliedArray': []
    //   };
    //   if (succeedArray.length > 0) {
    //     result.succeedArray = succeedArray;
    //   }
    //   if (faliedArray.length > 0) {
    //     result.faliedArray = faliedArray;
    //   }
    //   return result;
    // },
    setColor(status) {
      switch (status.toLowerCase()) {
        case 'passed':
          return 'success';
        case 'failed':
          return 'error';
        default:
          return 'warning';
      }
    },
    createBug() {
      this.creatBugTag = true;
    },
    associatedBug() {
      this.associatedBugTag = true;
    },
    async getBugList() {
      let params = {
        tid: this.$route.query.tid,
        tag: this.$route.query.tag,
        build_id: this.$route.query.build_id,
        secondary_type: this.secondarytype
      };
      const {code, data, message} = await api.get(AssociateBugUrl, params);
      if (parseInt(code, 10) === 200) {
        this.bugList = data;
        // console.log('this.bugTypeList', this.bugTypeList);
      } else {
        this.bugList = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getScenesList() {
      const {code, data, message} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.bugTypeList = data.bugTypeList;
        this.initData();
        // console.log('this.bugTypeList', this.bugTypeList);
      } else {
        this.bugTypeList = {};
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async handleSubmit(auto) {
      let formD = new FormData();
      // this.uploadList.forEach((file) => {
      //   formD.append('file', file);
      // });
      // 上传内容和图片 addForm 以及 formD
      formD.append('data', JSON.stringify(this.addForm));
      // 直接上传base64内容
      formD.append('images', JSON.stringify(this.tmpList));
      // 发送请求
      await api.postFile(BugUrl, formD);
      this.initData(auto);
      this.getBugList();
    },
    async handleAssociate(auto) {
      // 发送请求
      let formD = new FormData();
      formD.append('data', JSON.stringify(this.associateForm));
      await api.postFile(BugUrl, formD);
      this.initData(auto);
      this.getBugList();
    },
    cancelAssociate(auto) {
      this.initData(auto);
    },
    handleView(item) {
      this.images = item.content;
      this.visible = true;
    },
    getImageBs64(item) {
      var _base64 = '';
      const reader = new FileReader();
      reader.readAsDataURL(item);
      reader.onload = () => {
        _base64 = reader.result;
        this.tmpList.push({'name': item.name, 'content': _base64});
      };
    },
    handleRemove(name) {
      this.uploadList = this.uploadList.filter(item => {
        return item.name !== name;
      });
      this.tmpList = this.tmpList.filter(item => {
        return item.name !== name;
      });
    },
    handleFormatError(file) {
      this.$Notice.warning({
        title: 'The file format is incorrect',
        desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
      });
    },
    handleMaxSize(file) {
      this.$Notice.warning({
        title: 'Exceeding file size limit',
        desc: 'File ' + file.name + ' is too large, no more than 2M.'
      });
    },
    handleBeforeUpload(file) {
      const check = this.uploadList.length < 3;
      if (!check) {
        this.$Notice.warning({
          title: 'Up to five pictures can be uploaded.'
        });
      }
      this.uploadList.push(file);
      this.getImageBs64(file);
      return false;
    },
    handleReset(auto) {
      this.initData(auto);
    },
    initData(auto) {
      this.associatedBugTag = false;
      this.associateForm = {
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        tag: this.$route.query.tag,
        secondary_type: this.secondarytype,
        issues_url: ''
      };
      this.addForm = {
        secondary_type: this.secondarytype,
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        repo: this.$route.query.repo,
        bug_type: this.bugTypeList[this.$route.query.task_type],
        tag: this.$route.query.tag,
        title: '',
        description: '',
        level: 'P0',
        qa_owner: '',
        rd_owner: ''
      };
      // this.$refs['addForm'].resetFields();
      this.$emit('on-cancel', auto && auto.type === 'click' ? false : auto);
      this.creatBugTag = false;
      this.uploadList = [];
      this.defaultList = [];
      this.tmpList = [];
    }
  }
};
</script>

<style scoped>
  .all-line-row {
    margin-top: 1%;
    margin-bottom: 1%;
    margin-left: 1%;
    margin-right: 1%;
    font-size: 14px;
  }
  .scroll-cls {
    overflow-y: auto;
  }
  .center-card-s {
    width: 100%;
    max-height: 600px;
    overflow: auto;
    margin-bottom: 1%
  }
  .demo-upload-list-cover{
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,.6);
  }
  .demo-upload-list{
    display: inline-block;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0,0,0,.2);
    margin-right: 4px;
  }
  .demo-upload-list:hover .demo-upload-list-cover{
    display: block;
  }
  .demo-upload-list-cover i{
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
  }
  .demo-upload-list img{
    width: 100%;
    height: 100%;
  }
</style>

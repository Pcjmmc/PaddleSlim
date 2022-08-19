<template>
  <div>
    <Card class="center-card-s">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
          <Icon type="ios-information-circle" size="20"></Icon>
          {{ "任务信息概述" }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em; margin-top: 2%">
        任务名: {{ $route.query.tname }}
        <span style="float:right;">
          <ButtonGroup size="small">
            <Button type="text" @click="associatedBug()">关联卡片</Button>
            <Button type="text" @click="createBug()">新建卡片</Button>
          </ButtonGroup>
        </span>
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        repo信息: {{ $route.query.repo }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        commit信息: {{ $route.query.commit_id }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        commit提交时间: {{ changeTimestamp($route.query.commit_time) }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        分支信息: {{ $route.query.branch }}
      </p>
      <p slot="title" style="text-align: left;font-size: 1.0em;">
        执行时间: {{ changeTimestamp($route.query.created) }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: green"
        v-else
      >
        状态: {{ $route.query.status }}
      </p>
      <p
        slot="title"
        style="text-align: left;font-size: 1.0em;color: red"
        v-if="$route.query.status.toLowerCase()=='failed'"
      >
        原因: {{ getErrorReason($route.query.exit_code) }}
      </p>
    </Card>
    <Card
      :bordered="false"
      class="center-card-s"
      v-if="bugList.length > 0"
    >
      <p slot="title" style="text-align: center;font-size: 1.2em;">
        关联卡片
      </p>
      <icafe-base :datas="bugList"></icafe-base>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(env_info) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-document" size="20"></Icon>
        {{ "编译环境" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="env_info"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(compile_param) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-bookmarks" size="20"></Icon>
        {{ "编译参数" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="compile_param"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
    <Card class="center-card-s" v-if="JSON.stringify(gpu_arch) != '[]'">
      <p slot="title" style="text-align: center;font-size: 1.4em;">
        <Icon type="md-cloud-download" size="20"></Icon>
        {{ "产物详情" }}
      </p>
      <p>
        <Table
          border
          :columns="column"
          :data="gpu_arch"
          style="margin-right: 2%"
        >
        </Table>
      </p>
    </Card>
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
import Clipboard from 'clipboard';
import api from '../api/index';
import { dateFmt, timestampToTime } from '../util/help.js';
import { DetailUrl, BugUrl, ScenesUrl, AssociateBugUrl } from '../api/url.js';
import icafeBase from './Base/icafeBase.vue';

export default {
  data: function () {
    return {
      bugList: [],
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
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        tag: this.$route.query.tag,
        secondary_type: this.$route.query.secondary_type,
        issues_url: ''
      },
      addForm: {
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        secondary_type: this.$route.query.secondary_type,
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
      bugTypeList: {},
      detail: {},
      column: [
        {
          title: '选项',
          key: 'key'
        },
        {
          title: '取值',
          key: 'value',
          render: (h, params) => {
            var key = params.row.key;
            var value = params.row.value;
            let arr = [];
            var newArr = [];
            if (key === 'artifact_url') {
              if (value instanceof Array) {
                arr = value;
              } else {
                arr = [value];
              }
              arr.forEach((url, index) => {
                newArr.push(h('div', [
                  h('a', {
                    }, url),
                    h('Poptip', {
                      props: {
                        trigger: 'hover',
                        placement: 'top',
                        // 注意一定要添加该属性，否则表格会遮盖住气泡浮框
                        transfer: true,
                        content: '复制'
                      }
                    },
                    [
                      h('Icon', {
                        class: 'ivu-icon ivu-icon-ios-copy-outline copyBtn',
                        props: {
                            type: 'ios-copy-outline',
                            size: '20',
                            color: 'green'
                        },
                        on: {
                          click: () => {
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
                          }
                        }
                      })
                    ])
                  ])
                );
              });
            } else {
              newArr.push(
                h('div', [h('span', {}, value !== '' ? value : '—')
                ])
              );
            }
            return h('div', newArr);
          }
        }
      ],
      env_info: [],
      compile_param: [],
      gpu_arch: []
    };
  },
  mounted: function () {
    this.getData();
    this.getScenesList();
    this.getBugList();
  },
  components: {
    icafeBase
  },
  computed: {
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
    getColumn(obj) {
      let _columns = [];
      if (obj.length > 0) {
        let tmpobj = obj[0];
        for (let key in tmpobj) {
          if (tmpobj.hasOwnProperty(key)) {
            _columns.push(key);
          }
        }
      }
      let result = [];
      for (let idx = 0; idx < _columns.length; idx++) {
        let tmp = {
          title: _columns[idx],
          key: _columns[idx]
        };
        result.push(tmp);
      }
      // console.log(result);
      return result;
    },
    pocessData(obj) {
      let result = [];
      for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
          let tmp = {
            key: key,
            value: obj[key]
          };
          result.push(tmp);
        }
      }
      return result;
    },
    async getBugList() {
      let params = {
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        tag: this.$route.query.tag,
        secondary_type: this.$route.query.secondary_type
      };
      const {code, data, msg} = await api.get(AssociateBugUrl, params);
      if (parseInt(code, 10) === 200) {
        this.bugList = data;
      } else {
        this.bugList = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      // console.log('params is', this.$route.query);
      let _params = {
        'tid': this.$route.query.tid,
        'build_id': this.$route.query.build_id,
        'task_type': this.$route.query.task_type,
        'secondary_type': this.$route.query.secondary_type
      };
      // 自己知道自己值传递了一个secondary_type
      const { code, data, message } = await api.get(DetailUrl, _params);
      if (message === 'success') {
        for (let key in data) {
          if (data.hasOwnProperty(key)) {
            this.detail = data[key].case_detail;
            if (this.detail.length > 0) {
              this.env_info = this.pocessData(this.detail[0].env_info);
              this.compile_param = this.pocessData(this.detail[0].compile_param);
              this.gpu_arch = this.pocessData(this.detail[0].gpu_arch);
              this.gpu_arch.push({key: 'artifact_url', value: this.$route.query.artifact_url});
            }
          }
        }
      } else {
        console.log('code: ', code);
        this.$Message.error({content: message || this.$trans('获取编译列表失败'), duration: 5, closable: true});
      }
    },
    createBug() {
      this.creatBugTag = true;
    },
    associatedBug() {
      this.associatedBugTag = true;
    },
    async getScenesList() {
      const {code, data, msg} = await api.get(ScenesUrl);
      if (parseInt(code, 10) === 200) {
        this.bugTypeList = data.bugTypeList;
        this.initData();
        // console.log('this.bugTypeList', this.bugTypeList);
      } else {
        this.bugTypeList = {};
        this.$Message.error({
          content: '请求出错: ' + msg,
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
        secondary_type: this.$route.query.secondary_type,
        tid: this.$route.query.tid,
        build_id: this.$route.query.build_id,
        tag: this.$route.query.tag,
        issues_url: ''
      };
      this.addForm = {
        secondary_type: this.$route.query.secondary_type,
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
  .tips {
    color: #ff9900;
  }
  .all-line-row {
    margin-bottom: 0.5%;
    margin-left: 0.5%;
  }
  .center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
    margin-bottom: 2%
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

<template>
  <Card class="center-card-s">
    <Row align="middle">
      <Col :xs="{ span: 11, offset: 0 }">
        <div v-for="(item, key, index) in data" style="margin-top: 0.5%;">
          <span v-if="item.status && item.status.toLowerCase()=='passed'">
            <i-circle
              :percent="100"
              stroke-color="#5cb85c"
              :size="15"
            >
              <Icon
                type="ios-checkmark"
                size="10"
                style="color:#5cb85c"
              ></Icon>
            </i-circle>
              <a
                v-if="item.show_name"
                href="javascript:void(0)"
                style="font-size:13px;"
                @click="jumper(item)"
              > {{ item.show_name }} </a>
              <a
                v-else
                href="javascript:void(0)"
                style="font-size:13px;"
                @click="jumper(item)"
              > {{ item.tname }} </a>
            <!--
            <span style="font-size:13px;"> {{ item.tname }} </span>
            -->
          </span>
          <span v-else-if="item.status && item.status.toLowerCase()=='failed'">
            <i-circle
              :percent="100"
              stroke-color="#ff5500"
              :size="15"
            >
              <Icon
                type="ios-close"
                size="10"
                style="color:#ff5500"
              ></Icon>
            </i-circle>
            <Tooltip placement="right" :content="getErrorReason(item.exit_code)">
              <span
                v-if="item.show_name"
                style="font-size:13px;"
              > {{ item.tname }} </span>
              <span
                v-else
                style="font-size:13px;"
              > {{ item.tname }} </span>
            </Tooltip>
          </span>
          <span v-else-if="item.status && item.status.toLowerCase()=='running'">
            <Icon
              type="ios-loading"
              size="20"
              class="demo-spin-icon-load"
            ></Icon>
            <Tooltip placement="right" width="400">
              <span
                v-if="item.show_name"
                style="font-size:13px;"
              > {{ item.tname }} </span>
              <span
                v-else
                style="font-size:13px;"
              > {{ item.tname }} </span>
              <span
                slot="content"
                data-test="ring-dropdown"
                class="dropdown_40a"
              >
                <div
                  class="BuildDurationAnchor__buildDuration--tx
                  global__font-smaller--2q
                  global__font-lower--3X global__font--1w"
                >
                  <div
                    class="BuildDurationAnchor__wrapper--1R
                    global__font-smaller--2q
                    global__font-lower--3X global__font--1w"
                  >
                    <span class="BuildDurationAnchor__text--2P">{{ item.left_time }}</span>
                    <div class="BuildDurationAnchor__progress--2J" style="width: 19%;">
                      <div style="width: 526.316%;">
                        <span class="BuildDurationAnchor__text--2P">{{ item.left_time }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </span>
            </Tooltip>
          </span>
          <span v-else>
            <Tooltip placement="right" content="未执行">
              <Icon type="ios-alert-outline" size="17"/>
              <span
                v-if="item.show_name"
                style="font-size:13px;"
              > {{ item.show_name }} </span>
              <span
                v-else
                style="font-size:13px;"
              > {{ item.tname }} </span>
            </Tooltip>
          </span>
        </div>
      </Col>
      <!--
      <Col span="3">
        <div v-for="(item, key, index) in data" style="margin-top: 0.5%;">
          <span style="float:right;">
            <span style="color:green;" > {{ 50 }} </span>
            <span> | </span>
            <span style="color:red;" v-if="true"> {{ 2 }} </span>
            <span style="color:green;" v-else=""> {{ 2 }} </span>
          </span> 
        </div>
      </Col>
      -->
      <Col :xs="{ span: 1.5, offset: 2 }">
        <div v-for="(item, key, index) in data" style="margin-top: 0.5%;">
          <span style="float:right;">
           <a
            href="javascript:void(0)"
            @click="jumperLog(item.log_url)"
            style="font-size:13px;"
            > 日志 </a>
          </span> 
        </div>
      </Col>
      <Col :xs="{ span: 5, offset: 5 }" align="center">
        <div class="one-fifth-video-col">
          <div v-if="system.includes('Windows')">
            <Icon type="logo-windows" size="50"> </Icon>
           </div>
          <div v-else-if="system.includes('Mac')">
            <Icon type="logo-apple" size="50"> </Icon>
          </div>
          <div v-else>
            <Icon type="logo-tux" size="50"> </Icon>
          </div>
          <h4>{{ system }}</h4>
        </div>
      </Col>
    </Row>
    <div>
      <Modal v-model="setBugTagModal" title="快速创建bug卡片" @on-cancel="handleReset" width="600px">
        <Form ref="addForm" :model="addForm" :rules="addRules" :label-width="80">
          <FormItem label="所属计划: ">
            <Input v-model="tag"/>
          </FormItem>
          <FormItem label="卡片标题: " prop="title">
            <Input v-model="addForm.title"/>
          </FormItem>
          <FormItem label="等级" prop="level">
            <Select v-model="addForm.level" >
              <Option v-for="(item, index) in levelList" :value="item" :key="index">{{ item }}</Option>
            </Select>
          </FormItem>
          <FormItem label="rd负责人" prop="rd_owner">
            <Input v-model="addForm.rd_owner"/>
          </FormItem>
          <FormItem label="qa负责人" prop="qa_owner">
            <Input v-model="addForm.qa_owner"/>
          </FormItem>
          <FormItem label="详情描述: " prop="description">
            <Input v-model="addForm.description" type="textarea" :autosize="{minRows: 2,maxRows: 20}"/>
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
                <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
              </template>
            </div>
            <Upload
              ref="upload"
              :show-upload-list="false"
              :default-file-list="defaultList"
              :format="['jpg','jpeg','png']"
              :max-size="10240"
              :on-format-error="handleFormatError"
              :on-exceeded-size="handleMaxSize"
              :before-upload="handleBeforeUpload"
              multiple
              type="drag"
              action="/"
              style="display: inline-block;width:58px;">
              <div style="width: 58px;height:58px;line-height: 58px;">
                <Button icon="ios-camera"></Button>
              </div>
            </Upload>
            <Modal title="View Image" v-model="visible">
              <img :src="images" v-if="visible" style="width: 100%">
            </Modal>
          </FormItem>
        </Form>
        <div slot="footer">
          <Button type="text" @click="handleReset">取消</Button>
          <Button type="primary" @click="handleSubmit">确定</Button>
        </div>
      </Modal>
    </div>
  </Card>
</template>

<script>
import Modal from "../ModalSimple";
import { ExemptUrl, BugUrl } from '../../api/url.js';
import api from '../../api/index';
export default {
  name: 'compileBase',
  props: {
    'system': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'data': {
      type: [Array],
      default: function () {
        return [];
      }
    },
    'tag': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'versionid': {
      type: [Number],
      default: function () {
        return '';
      }
    },
    'versionname': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'index': {
      type: [Number],
      default: function () {
        return 0;
      }
    }
  },
  data: function () {
    return {
      images: '',
      setBugTagModal: false,
      visible: false,
      uploadList: [],
      tmpList: [],
      defaultList: [],
      levelList: [
        'P0',
        'P1',
        'P2',
        'P3'
      ],
      addForm: {
        title: '',
        description: '',
        level: 'P0',
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
      }
    };
  },
  mounted: function () {
    // console.log('data', this.data);
  },
  components: {
  },
  computed: {
    succeedNum() {
      let count = 0;
      for (var idx = 0; idx < this.data.length; idx++) {
        let item = this.data[idx];
        if (item.status && item.status.toLowerCase() === 'passed') {
          count += 1;
        }
      }
      return count;
    },
    totalNum() {
      return this.data.length;
    }
  },
  methods: {
    jumper(item) {
      // console.log('item is', item);
      // 还是根据任务的type来确定跳转到function还是model，目前暂时都用ApiDetails
      let _params = {
        task_type: item.task_type,
        tid: item.tid,
        build_id: item.build_id,
        secondary_type: item.secondary_type,
        status: item.status,
        exit_code: item.exit_code,
        repo: item.repo,
        branch: item.branch,
        commit_id: item.commit_id,
        tname: item.tname,
        created: item.created
      };
      // let _params = {};
      // _params = Object.assign(_params, item);
      // console.log('item', _params);
      let detail_name = '';
      if (item.reponame === 'Paddle2ONNX' || item.reponame === 'PaddleHub') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'model') {
        detail_name = 'model';
      } else if (item.task_type === 'frame') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'infer') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'dist') {
        // 如果二级分类是api的则跳转api详情页；否则按模型汇聚
        if (item.secondary_type.toLowerCase().includes('api')) {
          // console.log('secondary_type', item.secondary_type);
          detail_name = 'FuncDetail';
        } else {
          // console.log('model secondary_type', item.secondary_type);
          detail_name = 'model';
        }
      } else if (item.task_type === 'compile') {
          _params.artifact_url = item.artifact_url;
          detail_name = 'Compile';
      } else {
        return;
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
      window.open(href, '_blank');
    },
    jumperLog(url) {
      window.open(url, '_blank');
    },
    async createIcafe(item) {
      this.setBugTagModal = true;
    },
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
    handleReset(auto) {
      this.initData(auto);
    },
    initData(auto) {
      this.$refs['addForm'].resetFields();
      this.$emit('on-cancel', auto && auto.type === 'click' ? false : auto);
      this.setBugTagModal = false;
      this.uploadList = [];
      this.defaultList = [];
      this.tmpList = [];
    },
    async allowExempt(item, index) {
      Modal.confirm({
        title: '确认豁免任务',
        content: `${item.tname}</br>`,
        onOk: async () => {
          let params = {
            tid: item.tid,
            version_id: this.versionid,
            status: 1
          }
          const {code, msg} = await api.post(ExemptUrl, params);
          if (parseInt(code) == 200) {
            this.$set(this.data[index], 'exempt_status', true)
          } else {
            this.$Message.error({
              content: '请求出错: ' + msg,
              duration: 30,
              closable: true
            })
          }
        },
        onCancel: () => {
          this.$Message.info('点击取消')
        }
      })
    },
    async cancelExempt(item, index) {
      Modal.confirm({
        title: '确认取消豁免？',
        content: `${item.tname}</br>`,
        onOk: async () => {
          let params = {
            tid: item.tid,
            version_id: this.versionid,
            status: 0
          }
          const {code, msg} = await api.put(ExemptUrl, params);
          if (parseInt(code) == 200) {
            // 修改页面
            this.$set(this.data[index], 'exempt_status', false)
          } else {
            this.$Message.error({
              content: '请求出错: ' + msg,
              duration: 30,
              closable: true
            })
          }
        },
        onCancel: () => {
          this.$Message.info('点击取消')
        }
      })
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
    },
    handleView (item) {
      this.images = item.content;
      this.visible = true;
    },
    getImageBs64 (item) {
      var _base64 = '';
      const reader = new FileReader();
      reader.readAsDataURL(item);
      reader.onload = () => {
        _base64 = reader.result;
        this.tmpList.push({'name': item.name, 'content': _base64});
      };
    },
    handleRemove (name) {
      this.uploadList = this.uploadList.filter(item => {
        return item.name != name;
      })
      this.tmpList = this.tmpList.filter(item => {
        return item.name != name;
      })
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: 'The file format is incorrect',
        desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
      });
    },
    handleMaxSize (file) {
      this.$Notice.warning({
        title: 'Exceeding file size limit',
        desc: 'File ' + file.name + ' is too large, no more than 2M.'
      });
    },
    handleBeforeUpload (file) {
      const check = this.uploadList.length < 3;
      if (!check) {
        this.$Notice.warning({
          title: 'Up to five pictures can be uploaded.'
        });
      }
      this.uploadList.push(file);
      this.getImageBs64(file);
      return false;
    }
  }
};
</script>

<style scoped>
  .center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
    border-color:green;
  }
  .demo-spin-col{
    height: 100px;
    position: relative;
    border: 1px solid #eee;
  }
  .demo-spin-icon-load{
    animation: ani-demo-spin 1s linear infinite;
    color: blue;
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
  .dropdown_40a {
    display: inline-block;
  }
  .BuildDurationAnchor__buildDuration--tx {
    display: -webkit-inline-box;
    display: -ms-inline-flexbox;
    display: inline-flex;
    -webkit-box-align: baseline;
    -ms-flex-align: baseline;
    align-items: baseline;
    -webkit-box-pack: end;
    -ms-flex-pack: end;
    justify-content: flex-end;
    margin-left: -8px;
    padding-left: 8px;
    text-align: right;
    white-space: nowrap;
    font-weight: normal;
}
.global__font--1w {
    font-family: -apple-system, BlinkMacSystemFont, Ubuntu, "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    line-height: 20px;
}
.global__font-lower--3X {
    line-height: 18px;
}
.global__font-smaller--2q {
    font-size: 12px;
}
.BuildDurationAnchor__wrapper--1R {
  position: relative;
  z-index: 1;
  overflow: hidden;
  width: 112px;
  margin: 0;
  padding: 0 0 1px;
  cursor: default;
  white-space: nowrap;
  color: #428d00;
  border-radius: 3px;
  background-color: rgb(228, 241, 217);
}
.BuildDurationAnchor__progress--2J {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  overflow: hidden;
  height: 21px;
  text-align: right;
  color: white;
  border-radius: 3px 0 0 3px;
  background-color: #4DA400;
}
.BuildDurationAnchor__text--2P {
  padding-right: 8px;
}
.one-fifth-video-col {
  margin-right: 2%;
  margin-left: 2%;
  margin-bottom: 2%;
  margin-top: 2%;
}
</style>
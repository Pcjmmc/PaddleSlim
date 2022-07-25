<template>
  <div>
    <Card class="center-card-s">
      <Row type="flex" justify="start" class="code-row-bg">
        <Col class="float: left" flex="5">
          <Row>
            <Col
              span="8"
              v-for="(item, key, index) in data">
              <base-card
                :reponame="key"
                :data="item"
                :latestCommitTime="latestCommitTime"
              >
              </base-card>
            </Col>
          </Row>
        </Col>
        <Col flex="1" align="center">
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
    </Card>
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
  </div>
</template>

<script>
import baseCard from "./baseCard.vue";
import Modal from "../ModalSimple";
import { ExemptUrl, BugUrl } from '../../api/url.js';
import api from '../../api/index';
export default {
  name: 'modelBase',
  props: {
    'system': {
      type: [String],
      default: function () {
        return '';
      }
    },
    'data': {
      type: Object
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
    },
    'latestCommitTime': {
      type: [Number],
      default: function () {
        return null;
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
    // console.log('data', this.data)
  },
  components: {
    baseCard
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
      // 还是根据任务的type来确定跳转到function还是model，目前暂时都用ApiDetails
      let _params = {
        task_type: item.task_type,
        tid: item.tid,
        build_id: item.build_id,
        secondary_type: item.secondary_type,
        status: item.status,
        exit_code: item.exit_code
      };
      // _params = Object.assign(_params, item);
      // console.log('item', item)
      let detail_name = '';
      if (item.reponame === 'Paddle2ONNX' || item.reponame === 'PaddleHub') {
        detail_name = 'FuncDetail';
      } else if (item.task_type === 'model') {
        detail_name = 'model';
      } else if (item.task_type === 'lite') {
        detail_name = 'lite';
      } else {
        return;
      }
      const { href } = this.$router.resolve({name: detail_name, query: _params});
      window.open(href, '_blank');
    },
    async createIcafe(item) {
      this.setBugTagModal = true;
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
    max-height: 700px;
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
  display: table-cell;
  vertical-align: middle;
  text-align: center;
  height: 300px;
}
</style>
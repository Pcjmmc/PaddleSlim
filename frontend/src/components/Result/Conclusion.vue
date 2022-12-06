<template>
<div>
  <!-- <Row type="flex" justify="end">
    <Col span="2">
      <Button type="primary" @click="exportToPDF">导出</Button>
    </Col>
  </Row> -->
  <div>
    <div style="font-size:14px;">
      <span>
        <label> 所属计划: </label>
        <span v-if="tag"> {{ tag }} </span>
        <span v-else> {{ branch }} </span>
      </span>
    </div>
    <CheckboxGroup v-model="checkAllGroup">
      <div v-for="(item, index) in tasktypelist" style="margin-top: 1%;">
        <div v-if="item.key=='model'">
          <label> 套件兼容性:
            <Button
              size="small"
              type="info"
              icon="md-cloud-download"
              @click="showIcafe(item.key)"
            >load卡片</Button>
          </label>
          <div v-for="(repo, idx) in repoNames">
            <Checkbox :label="repo"> {{ repo }} </Checkbox>
            <Input
              clearable
              v-model="addForm[item.key][repo]"
              type="textarea"
              placeholder="描述风险"
              :autosize="{minRows: 2,maxRows: 30}"
            />
          </div>
        </div>
        <div v-else>
          <Checkbox :label="item.key"> {{ item.desc }}
            <!--
            <a href="javascript:void(0)" @click="showIcafe(item.key)">load卡片</a>
            -->
            <Button
              size="small"
              type="info"
              icon="md-cloud-download"
              @click="showIcafe(item.key)"
            >load卡片</Button>
          </Checkbox>
          <Input
            clearable
            v-model="addForm[item.key]"
            type="textarea"
            placeholder="描述风险"
            :autosize="{minRows: 2,maxRows: 30}"
          />
        </div>
        </Form>
      </div>
    </CheckboxGroup>
  </div>
  <div
    slot="footer"
    align="center"
    style="margin-top: 1%"
  >
    <Button type="warning" @click="handleReset">取消</Button>
    <Button type="primary" @click="handleSubmit">提交</Button>
  </div>
  <div>
    <Modal
      v-model="setBugTagModal"
      title="风险卡片"
      width="1200px"
      v-on:on-cancel="handleResetNew"
    >
      <icafe-base :datas="datas"></icafe-base>
      <div slot="footer">
        <Button type="text" @click="handleResetNew">关闭</Button>
      </div>
    </Modal>
  </div>
</div>
</template>

<script>
// import html2pdf from 'html2pdf.js';
import Cookies from 'js-cookie';
import api from '../../api/index';
import { TestConclusionUrl, BugUrl } from '../../api/url.js';
import icafeBase from '../Base/icafeBase.vue';

export default {
   props: {
    tasktypelist: {
      type: [Array],
      default: function () {
        return [];
      }
    },
    tag: {
      type: [String],
      default: function () {
        return '';
      }
    },
    branch: {
      type: [String],
      default: function () {
        return '';
      }
    }
  },
  data: function () {
    return {
      setBugTagModal: false,
      datas: [],
      checkAllGroup: [],
      addForm: {
        compile: '',
        frame: '',
        infer: '',
        dist: '',
        benchmark: '',
        doc: '',
        model: {
          PaddleClas: '',
          PaddleGAN: '',
          PaddleOCR: '',
          PaddleNLP: '',
          PaddleSeg: '',
          PaddleDetection: '',
          PaddleSpeech: '',
          PaddleRec: '',
          PaddleSlim: '',
          PaddleHub: '',
          Paddle2ONNX: '',
          PaddleScience: '',
          Xpu: ''
        }
      },
      repoNames: [
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
        'Xpu'
      ]
    };
  },
  mounted: function () {
    this.getData();
    // console.log('tasktypelist', this.tasktypelist);
  },
  watch: {
    versionName: function () {
      this.getData();
    }
  },
  components: {
    icafeBase
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version ? this.$store.state.version : this.$route.params.version;
      }
    }
  },
  methods: {
    showIcafe(task_type) {
      // console.log(task_type);
      this.getIcafe(task_type);
      this.setBugTagModal = true;
    },
    async getIcafe(task_type) {
      // 根据发现方式去获取TODO
      let _params = {version: this.versionName, task_type: task_type};
      const {code, data, message} = await api.get(BugUrl, _params);
      if (parseInt(code, 10) === 200) {
        this.datas = data;
      } else {
        this.datas = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getData() {
      this.resetData();
      if (!this.versionName) {
        return;
      }
      let params = {
        version: this.versionName,
        appid: Cookies.get('appid')
      };
      // 将数组用都好分割拼接
      const {code, data, message, all_count} = await api.get(TestConclusionUrl, params);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      } else {
        if (all_count !== 0) {
          this.addForm = data;
        }
      }
    },
    exportToPDF() {
      // html2pdf(this.$refs.document, {
      //   margin: 1,
      //   filename: 'conclusion.pdf',
      //   image: { type: 'jpeg', quality: 0.98 },
      //   html2canvas: { dpi: 192, letterRendering: true },
      //   jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape' }
      // })
    },
    handleReset(auto) {
      this.initData();
    },
    handleResetNew(auto) {
      this.datas = [];
      this.setBugTagModal = false;
    },
    resetData() {
      this.checkAllGroup = [];
      this.addForm = {
        compile: '',
        frame: '',
        model: {
          PaddleClas: '',
          PaddleGAN: '',
          PaddleOCR: '',
          PaddleNLP: '',
          PaddleSeg: '',
          PaddleDetection: '',
          PaddleSpeech: '',
          PaddleRec: '',
          PaddleSlim: '',
          PaddleHub: '',
          Paddle2ONNX: '',
          PaddleScience: '',
          Xpu: ''
        },
        infer: '',
        dist: '',
        benchmark: '',
        doc: ''
      };
    },
    initData() {
      this.resetData();
      this.getData();
    },
     handelUpdate(row) {
      this.selectedRow = row;
      this.updateModelFlag = true;
      this.sendType2 = this.sendTypeList[row.task_type];
    },
    async handleSubmit() {
      if (this.checkAllGroup.length === 0) {
        this.$Message.warning({
          content: '请勾选修改内容，再提交！',
          duration: 3,
          closable: true
        });
        return false;
      }
      let data = [];
      for (var idx = 0; idx < this.checkAllGroup.length; idx++) {
        let key = this.checkAllGroup[idx];
        let content = '';
        let task_type = '';
        let model_repo = '';
        if (key in this.addForm) {
          content = this.addForm[key];
          task_type = key;
          model_repo = '';
        } else {
          content = this.addForm.model[key];
          task_type = 'model';
          model_repo = key;
        }
        let record = {
          appid: Cookies.get('appid'),
          tag: this.tag,
          branch: this.branch,
          task_type: task_type,
          model_repo: model_repo,
          conclusion: content
        };
        data.push(record);
      }
      let params = {
        data: JSON.stringify(data)
      };
      // 将数组用都好分割拼接
      const {code, message} = await api.post(TestConclusionUrl, params);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
      this.getData();
      this.checkAllGroup = [];
    }
  }
};
</script>

<style scoped>
</style>

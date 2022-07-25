<template>
<div>
  <!-- <Row type="flex" justify="end">
    <Col span="2">
      <Button type="primary" @click="exportToPDF">导出</Button>
    </Col>
  </Row> -->
  <div>
    <div style="margin-top: 1%;margin-left: 7%">
      <span>
        <label> 所属计划: </label>
        <span v-if="tag"> {{ tag }} </span>
        <span v-else> {{ branch }} </span>
      </span>
    </div>
    <div v-for="(item, index) in tasktypelist" style="margin-top: 1%;margin-right: 2%">
      <Form
        :model="addForm"
        :label-width="150"
      >
        <FormItem :label="item.desc" :prop="item.key">
          <Input
            v-model="addForm[item.key]"
            type="textarea"
            placeholder="描述风险"
            :autosize="{minRows: 2,maxRows: 30}"
          />
        </FormItem>
      </Form>
    </div>
  </div>
  <div slot="footer" align="center">
    <Button type="warning" @click="handleReset">取消</Button>
    <Button type="primary" @click="handleSubmit">提交</Button>
  </div>
</div>
</template>

<script>
// import html2pdf from 'html2pdf.js';
import Cookies from 'js-cookie';
import api from '../../api/index';
import { TestConclusionUrl } from '../../api/url.js';

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
      addForm: {
        compile: '',
        frame: '',
        model: '',
        infer: '',
        dist: '',
        benchmark: '',
        doc: ''
      }
    };
  },
  mounted: function () {
    this.getData();
  },
  watch: {
    versionName: function () {
      this.getData();
    },
    branch: function () {
      this.getData();
    }
  },
  components: {
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    async getData() {
      let params = {
        tag: this.tag,
        branch: this.branch,
        appid: Cookies.get('appid')
      };
      // 将数组用都好分割拼接
      const {code, data, msg} = await api.get(TestConclusionUrl, params);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      } else {
        this.addForm = data;
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
    initData() {
      this.addForm = {
        compile: '',
        frame: '',
        model: '',
        infer: '',
        dist: '',
        benchmark: '',
        doc: ''
      };
      this.getData();
    },
     handelUpdate(row) {
      this.selectedRow = row;
      this.updateModelFlag = true;
      this.sendType2 = this.sendTypeList[row.task_type];
    },
    async handleSubmit() {
      let params = {
        tag: this.tag,
        branch: this.branch,
        compile: this.addForm.compile,
        frame: this.addForm.frame,
        model: this.addForm.model,
        infer: this.addForm.infer,
        dist: this.addForm.dist,
        benchmark: this.addForm.benchmark,
        doc: this.addForm.doc,
        appid: Cookies.get('appid')
      };
      // 将数组用都好分割拼接
      // console.log('up data job params is', params);
      const {code, msg} = await api.post(TestConclusionUrl, params);
      if (parseInt(code, 10) !== 200) {
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
      this.getData();
    }
  }
};
</script>

<style scoped>
</style>

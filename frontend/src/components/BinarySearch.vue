<template>
  <div class="one-fifth-video-col">
   <Form
      ref="addForm"
      :model="addForm"
      :rules="addRules"
      :label-width="85"
    >
      <span>
        <h3>欢迎使用二分查找工具，请输入二分条件!
         <a
          href="javascript:void(0)"
          style="font-size:13px;margin-left:2%;"
          @click="jumper('https://xly.bce.baidu.com/paddlepaddle/PR-Location/newipipe/builds/23574?module=github/PaddlePaddle/Paddle&pipeline=PR-Location&branch=branches')"
        > 效率云任务入口 </a>
      </h3>
      </span>
      <Row style="margin-top:2%;">
        <Col span="4">
          <FormItem label="repo:" prop="repo_name">
            <Select clearable v-model="addForm.repo_name">
              <Option
                :key="index"
                :value="item"
                v-for="(item, index) in Repos"
              >{{ item }}</Option>
            </Select>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="case名:" prop="model_name">
            <Input v-model="addForm.model_name" placeholder="输入模型或case名称"/>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="阶段名:" prop="step_name">
            <Input v-model="addForm.step_name" placeholder="输入阶段名称"/>
          </FormItem>
        </Col>
      </Row>
      <Row>
        <Col span="4">
          <FormItem label="问题类型:" prop="problem_type">
            <Select clearable v-model="addForm.problem_type">
              <Option
                :key="index"
                :value="item.key"
                v-for="(item, index) in problemType"
              >{{ item.desc }}</Option>
            </Select>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="时间:" prop="search_days">
            <Input v-model="addForm.search_days" placeholder="输入查找天数"/>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="关键字:" prop="key_word">
            <Input v-model="addForm.key_word" placeholder="输入失败关键字"/>
          </FormItem>
        </Col>
      </Row>
      <Row>
        <Col span="4">
          <FormItem label="基准值:" prop="baseline">
            <Input v-model="addForm.baseline" placeholder="基准值"/>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="阈值:" prop="threshold">
            <Input v-model="addForm.threshold" placeholder="阈值"/>
          </FormItem>
        </Col>
        <Col span="10">
          <FormItem label="邮箱:" prop="email_add">
            <Input v-model="addForm.email_add" placeholder="收取结果的邮箱地址"/>
          </FormItem>
        </Col>
      </Row>
      <Row justify="center">
        <Button type="primary" @click="handleSummit">确认并提交二分任务</Button>
      </Row>
    </Form>
    <Modal
      width="700px"
      v-model="show"
      title="任务链接"
      v-on:on-cancel="handleClose"
    >
      <div>
        <a
          href="javascript:void(0)"
          style="font-size:13px;margin-left:2%;"
          @click="jumper(joburl)"
        > {{ joburl }} </a>
      </div>
      <div slot="footer">
        <Button type="primary" @click="handleClose">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import { BinarySearchUrl } from '../api/url.js';
import api from '../api/index';

export default {
  name: 'binarySearch',
  data: function () {
    return {
      joburl: '',
      show: false,
      Repos: [
        'Paddle',
        'PaddleOCR',
        'PaddleNLP',
        'PaddleClas',
        'PaddleGAN',
        'PaddleSlim',
        'PaddleRec',
        'PaddleDetection',
        'PaddleSeg',
        'PaddleSpeech'
      ],
      problemType: [
        {
          key: '1',
          desc: '运行失败'
        },
        {
          key: '2',
          desc: '精度问题'
        },
        {
          key: '3',
          desc: '性能问题'
        },
        {
          key: '4',
          desc: '显存问题'
        }
      ],
      addForm: {
        repo_name: '',
        model_name: '',
        step_name: '',
        problem_type: '',
        search_days: '',
        key_word: '',
        threshold: '',
        email_add: ''
      },
      addRules: {
        repo_name: [
          { required: true, message: '请选择repo', trigger: 'blur' }
        ],
        model_name: [
          { required: true, message: '输入模型或case名称', trigger: 'blur' }
        ],
        problem_type: [
          { required: true, message: '请选择问题类型', trigger: 'blur' }
        ],
        search_days: [
          { required: true, message: '请输入查找天数', trigger: 'blur' }
        ],
        email_add: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' }
        ]
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.initData();
  },
  components: {
  },
  computed: {
  },
  methods: {
    handleSummit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.createJob();
        } else {
          this.$Message.error('请完善信息');
        }
      });
    },
    jumper(url) {
      window.open(url, '_blank');
    },
    initData() {
      this.addForm = {
        repo_name: '',
        model_name: '',
        step_name: '',
        problem_type: '',
        search_days: '',
        key_word: '',
        threshold: '',
        email_add: ''
      };
      this.joburl = '';
      this.show = false;
    },
    handleClose() {
      this.initData();
    },
    async createJob() {
      const {code, data, message} = await api.post(BinarySearchUrl, this.addForm);
      if (parseInt(code, 10) === 200) {
        this.joburl = data.url;
        this.show = true;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    }
  }
};
</script>

<style scoped>
.one-fifth-video-col {
  margin-right: 2%;
  margin-left: 2%;
  margin-bottom: 2%;
  margin-top: 2%;
}
</style>

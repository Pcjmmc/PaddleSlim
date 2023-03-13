<template>
  <div class="one-fifth-video-col">
    <Form
      ref="submitData"
      :model="submitData"
      :rules="addRules"
    >
      <Row>
        <h3>Wheel包链接：</h3>
        <Col span="10">
          <FormItem prop="wheel_link" style="font-size: large">
            <input
              v-model="submitData.wheel_link"
              placeholder="输入wheel包地址"
              style="width: 500px; height: 40px; font-size: small"
            >
          </FormItem>
        </Col>
      </Row>
      <h3>配置选取：</h3>
      <span
        class="font-success"
        style="font-size: medium"
      >
        (选择你想要测试的api-benchmark配置yaml)
      </span>
      <span
        style="display: inline"
      >
        使用默认配置：
      </span>
      <input
        type="radio"
        v-model="submitData.yaml_type"
        value="1"
      >
      <label>是</label>
      <input
        type="radio"
        v-model="submitData.yaml_type"
        value="0"
      >
      <label>否</label>
      <span style="display: inline">默认配置体量：</span>
      <Select
        clearable
        v-model="submitData.yaml_info"
        style="margin-right: 15px; width: 150px; height: 40px"
        :disabled="isDefault()"
      >
        <Option
          :key="index"
          :value="index"
          v-for="(item, index) in defaultSize"
          >
          {{ item }}
        </Option>
      </Select>

      <h3>自定义配置：</h3>
      <Select
        clearable
        v-model="submitData.yamlChoose"
        style="margin-right: 15px; width: 150px; height: 40px"
        :disabled="!isDefault()"
      >
        <Option
          :key="index"
          :value="index"
          v-for="(item, index) in Yamls"
        >
        {{ item }}
      </Option>
      </Select>
      <br />
      <textarea
        v-model="submitData.yamlContent"
        style="
          margin-right: 15px;
          width: 1000px;
          height: 200px;
          font-size: small;
        "
        placeholder="在此编辑测试用例"
        :disabled="!isDefault()"
      >
      </textarea>
      <br />
      <br />

      <h3>测试选项：</h3>
      <input
        type="radio"
        v-model="submitData.enable_backward"
        value="1"
        style="margin: 30px; margin-left: 15%"
      >
        <label>开启反向</label>
      <input
        type="radio"
        v-model="submitData.with_gpu"
        value="1"
        style="margin: 30px"
      >
        <label>GPU</label>
      <input
        type="radio"
        v-model="submitData.framework"
        value="1"
        style="margin: 30px"
      >
        <label>Paddle</label>
      <input
        type="radio"
        v-model="submitData.enable_backward"
        value="0"
        style="margin: 30px; margin-left: 15%"
      >
        <label>关闭反向</label>
      <input
        type="radio"
        v-model="submitData.with_gpu"
        value="0"
        style="margin: 30px"
      >
        <label>CPU</label>
      <input
        type="radio"
        v-model="submitData.framework"
        value="0"
        style="margin: 30px"
      >
        <label>Torch</label>

      <h3>cuda版本：</h3>
      <Select
        clearable
        v-model="submitData.cuda"
        style="margin-right: 15px; width: 150px; height: 40px"
      >
        <Option
          :key="index"
          :value="item"
          v-for="(item, index) in CudaVersion"
        >
          {{ item }}
        </Option>
      </Select>
      <h3>python版本：</h3>
      <Select
        clearable
        v-model="submitData.python"
        style="margin-right: 15px; width: 150px; height: 40px"
      >
        <Option
          :key="index"
          :value="item"
          v-for="(item, index) in PythonVersion"
        >
          {{ item }}
        </Option>
      </Select>

      <h3>备注Comment：</h3>
      <input
        v-model="submitData.comment"
        placeholder="请输入备注"
        style="margin-right: 15px; width: 1000px; font-size: small"
      >
      <Button
        class="btn-success"
        style="margin-left: 25%"
        @click="handleSummit"
      >
        点击执行效率云任务
      </Button>
    </Form>
  </div>
</template>

<script>
import { BenchmarkExec } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'BenchmarkExec',
  data: function () {
    return {
      joburl: '',
      checkDefault: true,
      show: false,
      submitData: {
        wheel_link: '',
        yaml_type: '',
        yaml_info: '',
        enable_backward: '',
        with_gpu: '',
        framework: '',
        yamlChoose: '',
        yamlContent: '',
        cuda: '',
        python: '',
        comment: '',
      },
      defaultSize: ['小kernel', '中kernel', '大kernel', '全部kernel'],
      Yamls: ['在线读取yaml', '本地上传yaml', '在线编辑yaml'],
      CudaVersion: ['v11.6', 'v11.2', 'v10.2'],
      PythonVersion: ['3.10', '3.9', '3.8', '3,7', '3.6'],
      addRules: {
        wheel_link: [
          { required: true, message: 'Wheel包链接不能为空', trigger: 'blur' },
        ],
      },
    };
  },
  mounted: function () {
    this.initData();
  },
  methods: {
    isDefault() {
      return this.submitData.yaml_type === 0;
    },
    handleSummit() {
      this.$refs.submitData.validate((valid) => {
        if (valid) {
          this.createJob();
        } else {
          this.$Message.error('请完善信息');
        }
      });
    },
    initData() {
      this.submitData = {
        wheel_link: '',
        yaml_type: 1,
        yaml_info: 0,
        enable_backward: 1,
        with_gpu: 1,
        framework: 1,
        yamlChoose: 1,
        yamlContent: '',
        cuda: 'v11.6',
        python: '3.8',
        comment: '',
      };
      this.joburl = '';
      this.show = false;
    },
    handleClose() {
      this.initData();
    },
    async createJob() {
      const { code, data, message } = await api.post(
        BenchmarkExec,
        this.submitData
      );
      if (parseInt(code, 10) === 200) {
        this.show = true;
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true,
        });
      }
    },
  },
};
</script>

<style scoped>
.one-fifth-video-col {
  margin-right: 1%;
  margin-left: 10%;
  margin-bottom: 1%;
  margin-top: 1%;
  font-size: 20px;
}
.btn-success {
  color: #fff;
  background-color: #6cf;
  border-color: #fff;
  font-size: larger;
}
.font-success {
  color: #0c27ed;
}
</style>

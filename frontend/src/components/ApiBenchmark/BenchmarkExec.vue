<template>
  <div class="one-fifth-video-col">
    <Form
      ref="submitData"
      :model="submitData"
      :rules="addRules"
    >
      <FormItem prop="comment">
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              任务名:
            </label>
          </Col>
          <Col>
            <Input
              placeholder="输入任务名(中间不要有空格)"
              style="width:200px"
              clearable
              v-model="submitData.comment"
            ></Input>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
        type="flex"
        align="middle"
        :gutter="8"
      >
          <Col span="6">
            <label>
              对比基线:
            </label>
          </Col>
          <Col>
            <label>
              Develop
            </label>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              Framework:
            </label>
          </Col>
          <Col>
            <RadioGroup v-model="submitData.framework">
               <Radio label="0">Paddle</Radio>
               <Radio label="1" disabled>Torch</Radio>
            </RadioGroup>
          </Col>
        </Row>
      </FormItem>

      <FormItem prop="wheel_link">
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col>
            <Input
              placeholder="请输入Paddle的whl包地址或版本号/Torch的版本号"
              clearable
              style="width:200%"
              v-model="submitData.wheel_link"
            ></Input>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              Python:
            </label>
          </Col>
          <Col>
            <Select
              v-model="submitData.python"
              size="small"
            >
              <Option
                :key="index"
                :value="index"
                v-for="(item, index) in PythonVersion"
              >
                {{ item }}
              </Option>
          </Select>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              OS:
            </label>
          </Col>
          <Col>
            <label>
              Linux
            </label>
          </Col>
        </Row>
      </FormItem>


      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              Place:
            </label>
          </Col>
          <Col>
            <RadioGroup v-model="submitData.place">
               <Radio label="0">CPU</Radio>
               <Radio label="1">GPU</Radio>
            </RadioGroup>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              CUDA:
            </label>
          </Col>
          <Col>
            <Select
              v-model="submitData.cuda"
              size="small"
            >
              <Option
                :key="index"
                :value="index"
                v-for="(item, index) in CudaVersion"
              >
                {{ item }}
              </Option>
          </Select>
          </Col>
        </Row>
      </FormItem>


      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              开启反向:
            </label>
          </Col>
          <Col>
            <RadioGroup v-model="submitData.enable_backward">
               <Radio label="0">是</Radio>
               <Radio label="1">否</Radio>
            </RadioGroup>
          </Col>
        </Row>
      </FormItem>

      <FormItem>
        <Row
          type="flex"
          align="middle"
          :gutter="8"
        >
          <Col span="6">
            <label>
              Kernel大小:
            </label>
          </Col>
          <Col>
            <Select
              v-model="submitData.yaml_info"
              size="small"
            >
              <Option
                :key="index"
                :value="index"
                v-for="(item, index) in defaultSize"
              >
                {{ item }}
              </Option>
          </Select>
          </Col>
        </Row>
      </FormItem>
    </Form>
  </div>
</template>

<script>
import { BenchmarkExec } from '../../api/url.js';
import api from '../../api/index';

export default {
    name: 'BenchmarkExec',
    data: function () {
      const validateWheelLink = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('此项不能为空（暂不支持Torch）'));
        } else {
          callback();
        }
      };
      const validateComment = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入任务名'));
        } else if (value.includes(' ')) {
          callback(new Error('任务名中不能含有空格'));
        } else {
          callback();
        }
      };
        return {
            joburl: '',
            checkDefault: true,
            show: true,
            submitData: {
                wheel_link: '',
                yaml_type: '0',
                yaml_info: '',
                enable_backward: '',
                place: '',
                framework: '',
                cuda: '',
                python: '',
                comment: '',
                system: '0'
            },
            framework_option: [
                'paddle',
                'torch'
            ],
            defaultSize: [
                '小kernel',
                '中kernel',
                '大kernel',
                '全部kernel'
            ],
            Yamls: [
                '在线读取yaml',
                '本地上传yaml',
                '在线编辑yaml'
            ],
            CudaVersion: [
                'v11.2',
                'v11.6'
            ],
            PythonVersion: [
                '3.7',
                '3.8',
                '3.9'
            ],
            addRules: {
                wheel_link: [
                    { validator: validateWheelLink, trigger: 'blur' }
                ],
                comment: [
                    { validator: validateComment, trigger: 'blur' }
                ]
            }
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
                comment: '',
                framework: '0',
                wheel_link: '',
                python: 0,
                system: '0',
                place: '1',
                cuda: 1,
                yaml_type: '0',
                yaml_info: 0,
                enable_backward: '0'
            };
        },
        handleClose() {
            this.initData();
        },
        async createJob() {
            const { code, _, message } = await api.post(BenchmarkExec, this.submitData);
            if (parseInt(code, 10) === 200) {
                this.show = false;
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
  margin-right: 1%;
  margin-left: 1%;
  margin-bottom: 1%;
  margin-top: 1%;
  font-size: 14px;
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

<template>
  <div class="demo-split">
    <Split v-model="split1">
      <div slot="left" class="all-line-row">
        <div class="main">
          <p align="left"> 请选择测试环境 </p>
        </div>
        <Form
          ref="addForm"
          :model="search"
          :rules="addRules"
          :label-width="75"
        >
          <FormItem label="任务名:" prop="name">
            <Input v-model="search.name" placeholder="输入任务名"/>
          </FormItem>
          <FormItem label="系统:" prop="os">
            <Select clearable v-model="search.os">
              <Option
                :key="index"
                :value="item"
                v-for="(item, index) in os"
              >{{ item }}</Option>
            </Select>
          </FormItem>
          <Row>
            <Col span="8">
              <FormItem label="类型:" prop="type">
                <Select clearable v-model="search.type">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in testType"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="16">
              <FormItem label="取值:" prop="value">
                <Input v-model="search.value" placeholder="输入 pr、commit 或 包地址"/>
              </FormItem>
            </Col>
          </Row>
          <FormItem
            label="分支:"
            prop="branch"
            :rules="{ required: true, message: '请选择分支', trigger: 'blur' }"
            v-if="search.type == 'pr'"
          >
            <Select clearable v-model="search.branch">
              <Option
                :key="index"
                :value="item"
                v-for="(item, index) in branch"
              >{{ item }}</Option>
            </Select>
          </FormItem>
          <FormItem label="cuda:" prop="cuda">
            <Select clearable v-model="search.cuda">
              <Option
                :key="index"
                :value="item"
                v-for="(item, index) in cuda"
              >{{ item }}</Option>
            </Select>
          </FormItem>
          <FormItem label="python:" prop="python">
            <Select clearable v-model="search.python">
              <Option
                :key="index"
                :value="item"
                v-for="(item, index) in python"
              >{{ item }}</Option>
            </Select>
          </FormItem>
        </Form>
        <Card
          bordered
          class="center-card-s"
          v-if="selectData.length > 0"
        >
          <p slot="title" style="color:green;"> 选中的测试内容: </p>
          <span
            :key="index"
            span="6"
            v-for="(item, index) in selectData"
          >
            <Button
              shape="circle"
              :style="{backgroundColor: randomColor()}"
              class="one-fifth-video-col"
            >
              <p style="color: white;"> {{ item.title }} </p>
            </Button>
          </span>
        </Card>
      </div>
      <div slot="right" class="main">
        <Row>
          <Col span="12" align="left">
            <p align="left"> 请选择测试内容 </p>
          </Col>
          <Col span="11" align="right">
            <Button type="primary" @click="handleSummit"> 提交 </Button>
          </Col>
        </Row>
        <Tree
          :data="data2"
          show-checkbox multiple
          :render="renderContent"
          v-on:on-check-change="SelectChange"
        ></Tree>
      </div>
    </Split>
    <Modal
      width="20px"
      v-model="show"
      title="任务详情"
      v-on:on-cancel="handleClose"
    >
      <div>
        <p>任务id:  {{ jobid }} </p>
        <p>任务名:  {{ search.name }} </p>
      </div>
      <div slot="footer">
        <Button type="primary" @click="handleClose">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import { FrameWorkConfigUrl, FrameWorkJobUrl } from '../../api/url.js';
import api from '../../api/index';

export default {
  name: 'testservice',
  data: function () {
    return {
      show: false,
      colorList: ['#EDE234', '#F78436',
        '#E03DE0', '#366EF7', '#33F083',
        '#F20CBD', '#0D36FC', '#00E679',
        '#FFFE00', '#F57E0F', '#F0BF00',
        '#F73700', '#9F00E0', '#007EF7',
        '#00F038', '#F0A700', '#F71400',
        '#6500E0', '#00BEF7', '#0DF000',
        '#F06E00', '#F700AF', '#0113E0',
        '#00F7AB', '#B2F000'
      ],
      search: {
        name: '',
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: ''
      },
      addRules: {
        name: [
          { required: true, message: '请输入任务名', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择类型', trigger: 'blur' }
        ],
        value: [
          { required: true, message: '请输入pr、commit 或包地址', trigger: 'blur' }
        ],
        cuda: [
          { required: true, message: '请选择cuda版本', trigger: 'blur' }
        ],
        os: [
          { required: true, message: '请选择系统环境', trigger: 'blur' }
        ],
        python: [
          { required: true, message: '请选择python版本', trigger: 'blur' }
        ]
      },
      jobid: '',
      selectData: [],
      content: [],
      split1: 0.4,
      branch: [
      ],
      cuda: [
      ],
      os: [
      ],
      python: [
      ],
      testType: [
      ],
      data2: [
        {
          title: 'API功能测试',
          key: 'api_function',
          expand: true,
          children: [
            {
              title: '计算op精度测试',
              key: 'op_function'
            },
            {
              title: '功能性API测试',
              key: 'external_api_function'
            },
            {
              title: 'IO相关测试',
              key: 'io_function'
            },
            {
              title: '分布式API测试',
              key: 'distribution_api_function'
            }
          ]
        },
        {
          title: '动转静测试',
          key: 'jit_function',
          expand: true,
          children: [
            {
              title: '动转静API单独组网测试',
              key: 'jit_api_function'
            },
            {
              title: '动转静模型子结构测试',
              key: 'jit_models_function'
            }
          ]
        },
        {
          title: 'API性能测试',
          key: 'api_benchmark',
          expand: true
        },
        {
          title: '模型测试',
          key: 'models',
          expand: true,
          children: [
            {
              title: '图像识别',
              key: 'paddleclas'
            }
          ]
        },
        {
          title: '模型性能测试',
          key: 'models_benchmark',
          expand: true
        },
        {
          title: '预测部署',
          key: 'infer',
          expand: true
        }
      ]
    };
  },
  watch: {
  },
  mounted: function () {
    this.initData();
    this.getSelectDatas();
  },
  components: {
  },
  computed: {
  },
  methods: {
    randomColor() {
      return this.colorList[Math.floor(Math.random() * this.colorList.length)];
    },
    handleClose() {
      this.initData();
    },
    SelectChange(data) {
      this.selectData = [];
      this.content = [];
      for (let idx = 0; idx < data.length; idx++) {
        let item = data[idx];
        if (item.children && item.children.length > 0) {
          continue;
        } else {
          this.selectData.push(item);
          this.content.push(item.key);
        }
      }
    },
    initData() {
      this.show = false;
      this.selectData = [];
      this.content = [];
      this.search = {
        name: '',
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: ''
      };
    },
    async getSelectDatas() {
      const {code, data, msg} = await api.get(FrameWorkConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.branch = data.branch;
        this.cuda = data.cuda;
        this.os = data.os;
        this.python = data.python;
        this.testType = data.type;
      } else {
        this.branch = [];
        this.cuda = [];
        this.os = [];
        this.python = [];
        this.testType = [];
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    handleSummit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.createJob();
        } else {
          this.$Message.error('请完善信息');
        }
      });
    },
    async createJob() {
      let params = {
        name: this.search.name,
        type: this.search.type,
        value: this.search.value,
        python: this.search.python,
        cuda: this.search.cuda,
        os: this.search.os,
        mission: JSON.stringify(this.content)
      };
      const {code, data, msg} = await api.post(FrameWorkJobUrl, params);
      if (parseInt(code, 10) === 200) {
        this.jobid = data.jid;
        this.show = true;
      } else {
        this.show = false;
        this.$Message.error({
          content: '请求出错: ' + msg,
          duration: 30,
          closable: true
        });
      }
    },
    renderContent(h, { root, node, data }) {
      if (node.children && node.children.length > 0) {
        return h('div', [
          h('Icon', {
            props: {
                type: 'ios-folder-outline'
            },
            style: {
                marginRight: '8px'
            }
          }),
          h('tag', {
            style: {
              'font-size': '20px',
              'line-height': '24px',
              height: '30px',
              border: '1px solid',
              background: 'lightblue'
            }
          }, data.title)
        ]);
      } else {
        return h('div', [
          h('Icon', {
            props: {
              type: 'ios-paper-outline'
            },
            style: {
              marginRight: '8px'
            }
          }),
          h('tag', {
            style: {
              'font-size': '20px',
              'line-height': '24px',
              height: '30px',
              border: '1px solid',
              background: 'lightblue'
            }
          }, data.title)
        ]);
      }
    }
  }
};
</script>

<style scoped>
.demo-split{
  height: 861px;
  overflow:auto;
}
.demo-split-pane{
  padding: 10px;
  text-align:center
}
.demo-tree {
  width: 100%;
  line-height: 2;
}
.one-fifth-video-col {
  margin-right: 2px;
  margin-left: 2px;
  margin-bottom: 2px;
  margin-top: 2px;
}
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow:auto;
  border-color:green;
  font-size: 16px;
  color:lightslategrey
}
.main {
  color:lightslategrey;
  margin-left: 2%;
  margin-top: 1%;
  margin-bottom: 2%;
  font-size: 20px;
  align: center;
}
.all-line-row {
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 2%;
  margin-top: 1%;
}
</style>

<style>
.ivu-tree ul {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 20px;
}
.ivu-tree-title {
  display: inline-block;
  margin: 0;
  padding: 0 4px;
  border-radius: 3px;
  cursor: pointer;
  vertical-align: top;
  -webkit-transition: all .2s ease-in-out;
  transition: all .2s ease-in-out;
}
</style>
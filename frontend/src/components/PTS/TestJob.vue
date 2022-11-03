<template>
  <div>
    <Card class="center-card-s">
      <p slot="title">环境配置</p>
      <Form
        ref="addForm"
        :model="search"
        :rules="addRules"
      >
        <FormItem
          prop="name"
        >
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                任务名:
              </label>
            </Col>
            <Col span="20">
              <Input
                v-model="search.name"
                placeholder="输入测试任务名"
                style="width:40%"
              ></Input>
            </Col>
          </Row>
        </FormItem>
        <div v-if="os.length > 0">
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                系统:
              </label>
            </Col>
            <Col span="20">
              <span v-for="item, index in os">
                <span v-if="item.checked">
                  <Tag
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'os')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
                <span v-else>
                  <Tag
                    checkable
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'os')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
              </span>
            </Col>
          </Row>
        </div>
        <div style="margin-top: 1%;" v-if="branch.length > 0">
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                分支:
              </label>
            </Col>
            <Col span="20">
              <span v-for="item, index in branch">
                <span v-if="item.checked">
                  <Tag
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'branch')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
                <span v-else>
                  <Tag
                    checkable
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'branch')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
              </span>
            </Col>
          </Row>
        </div>
        <div style="margin-top: 1%;" v-if="cuda.length > 0">
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                cuda:
              </label>
            </Col>
            <Col span="20">
              <span v-for="item, index in cuda">
                <span v-if="item.checked">
                  <Tag
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'cuda')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
                <span v-else>
                  <Tag
                    checkable
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'cuda')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
              </span>
            </Col>
          </Row>
        </div>
        <div style="margin-top: 1%;" v-if="python.length > 0">
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                python:
              </label>
            </Col>
            <Col span="20">
              <span v-for="item, index in python">
                <span v-if="item.checked">
                  <Tag
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'python')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
                <span v-else>
                  <Tag
                    checkable
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'python')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
              </span>
            </Col>
          </Row>
        </div>
        <div style="margin-top: 1%;" v-if="testType.length > 0">
          <Row type="flex" align="middle">
            <Col span="2" align="center">
              <label style="font-size:16px;">
                类型:
              </label>
            </Col>
            <Col span="20">
              <span v-for="item, index in testType">
                <span v-if="item.checked">
                  <Tag
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'testType')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
                <span v-else>
                  <Tag
                    checkable
                    :checked="item.checked"
                    color="primary"
                    v-on:on-change="changeTagStatus(item, 'testType')"
                  >
                    <font size="3"> {{ item.desc }}</font>
                  </Tag>
                </span>
              </span>
            </Col>
          </Row>
        </div>
        <div style="margin-top: 1%;" v-if="testType.length > 0">
          <FormItem
            prop="value"
          >
            <Row type="flex" align="middle">
              <Col span="2" align="center">
                <label style="font-size:16px;">
                  取值:
                </label>
              </Col>
              <Col span="20">
                <Input
                  v-model="search.value"
                  placeholder="输入pr、commit、version或者wheel包"
                  style="width:40%"
                ></Input>
              </Col>
            </Row>
          </FormItem>
        </div>
      </Form>
    </Card>
    <Card class="new-card-s">
      <div align="center" style="margin-top: 1%;">
        <tree-transfer
          open-all
          :title="title"
          :from_data="data2"
          :to_data="toData"
          :default-props="{label:'label'}"
          mode="transfer"
          height="600px"
          width="100%"
          @add-btn="add"
          @remove-btn="remove"
        ></tree-transfer>
      </div>
    </Card>
  </div>
</template>

<script>
import api from '../../api/index';
import treeTransfer from 'el-tree-transfer';
import { FrameWorkConfigUrl, FrameWorkJobUrl } from '../../api/url.js';

export default {
  name: 'TestJob',
  data: function () {
    return {
      title: ['测试场景', '已选测试项'],
      originToData: [],
      toData: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      addRules: {
        value: [
          { required: true, message: '请输入pr、commit 或包地址', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入任务名', trigger: 'blur' }
        ]
      },
      searchinit: {
      },
      branchinit: [],
      cudainit: [],
      osinit: [],
      pythoninit: [],
      testTypeinit: [],
      search: {
        name: '',
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: ''
      },
      content: [],
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
      data2: [],
      originData: [
        {
          id: '1',
          label: 'API功能测试',
          key: 'api_function',
          children: [
            {
              pid: '1',
              id: '1-1',
              label: '计算op精度测试',
              key: 'op_function'
            },
            {
              pid: '1',
              id: '1-2',
              label: '功能性API测试',
              key: 'external_api_function'
            },
            // {
            //   pid: '1',
            //   id: '1-3',
            //   label: 'IO相关测试',
            //   key: 'io_function'
            // },
            {
              pid: '1',
              id: '1-4',
              label: '分布式API测试',
              key: 'distribution_api_function'
            }
          ]
        },
        {
          id: '2',
          label: '动转静测试',
          key: 'jit_function',
          children: [
            {
              pid: '2',
              id: '2-1',
              label: 'JIT API单独组网测试',
              key: 'jit_function'
            },
            {
              pid: '2',
              id: '2-2',
              label: 'JIT 模型子结构测试',
              key: 'jit_models_function'
            }
          ]
        },
        {
          id: '3',
          label: '预测部署',
          key: 'infer',
          children: [
            {
              pid: '3',
              id: '3-1',
              label: '原生推理',
              key: 'native_infer'
            },
            {
              pid: '3',
              id: '3-2',
              label: 'TensorRT推理',
              key: 'trt_infer'
            },
            {
              pid: '3',
              id: '3-3',
              label: 'MKLDNN推理',
              key: 'mkldnn_infer'
            }
          ]
        },
        // {
        //   id: '4',
        //   label: '模型测试',
        //   key: 'models',
        //   children: [
        //     {
        //       pid: '4',
        //       id: '4-1',
        //       label: '图像识别',
        //       key: 'paddleclas'
        //     }
        //   ]
        // },
        {
          id: '5',
          label: '模型性能测试',
          key: 'models_benchmark',
          children: [
            {
              pid: '5',
              id: '5-1',
              label: 'V100',
              key: 'V100',
              children: [
                {
                  pid: '5-1',
                  id: '5-1-1',
                  label: '单机性能测试',
                  key: 'models_benchmark_v100_single_dp'
                },
                {
                  pid: '5-1',
                  id: '5-1-2',
                  label: '多机性能测试',
                  key: 'models_benchmark_v100_multi_dp'
                },
                {
                  pid: '5-1',
                  id: '5-1-3',
                  label: '分布式Collective模式性能测试',
                  key: 'models_benchmark_v100_dist_collective'
                },
                {
                  pid: '5-1',
                  id: '5-1-4',
                  label: '分布式Collective模式精度测试',
                  key: 'distribution_v100_accuracy_collective'
                }
              ]
            },
            {
              pid: '5',
              id: '5-2',
              label: 'A100',
              key: 'A100',
              children: [
                {
                  pid: '5-2',
                  id: '5-2-1',
                  label: '单机性能测试',
                  key: 'models_benchmark_a100_single_dp'
                },
                {
                  pid: '5-2',
                  id: '5-2-2',
                  label: '多机性能测试',
                  key: 'models_benchmark_a100_multi_dp'
                }
              ]
            }
          ]
        }
        // {
        //   id: '6',
        //   label: 'API性能测试',
        //   key: 'api_benchmark'
        // },
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
    treeTransfer
  },
  computed: {
  },
  methods: {
    handleClose() {
      this.initData();
    },
    SelectChange(data) {
      for (let idx = 0; idx < data.length; idx++) {
        let item = data[idx];
        if (item.children && item.children.length > 0) {
          // 递归遍历
          this.SelectChange(item.children);
        } else {
          this.content.push(item.key);
        }
      }
    },
    add(data2, toData, obj) {
      // 将选中的加入toData
    },
    // 监听穿梭框组件移除
    remove(data2, toData, obj) {
    },
    async handleSubmit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.createJob();
          // 调用父组件
          this.$emit('closeModal', false);
          this.$emit('searchByfilter');
          // 重置窗口
          this.initData();
        } else {
          this.$Message.error('请完善信息');
          // 调用父组件
        }
      });
    },
    initData() {
      this.toData = JSON.parse(JSON.stringify(this.originToData));
      this.data2 = JSON.parse(JSON.stringify(this.originData));
      this.branch = JSON.parse(JSON.stringify(this.branchinit)); // 记录下初始状态
      this.cuda = JSON.parse(JSON.stringify(this.cudainit)); // 记录下初始状态
      this.os = JSON.parse(JSON.stringify(this.osinit)); // 记录下初始状态
      this.python = JSON.parse(JSON.stringify(this.pythoninit)); // 记录下初始状态
      this.testType = JSON.parse(JSON.stringify(this.testTypeinit)); // 记录下初始状态
      this.search = JSON.parse(JSON.stringify(this.searchinit));
      this.content = [];
    },
    async getSelectDatas() {
      const {code, data, msg} = await api.get(FrameWorkConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.branch = this.processData(data.branch);
        this.branchinit = JSON.parse(JSON.stringify(this.branch)); // 记录下初始状态
        this.cuda = this.processData(data.cuda);
        this.cudainit = JSON.parse(JSON.stringify(this.cuda)); // 记录下初始状态
        this.os = this.processData(data.os);
        this.osinit = JSON.parse(JSON.stringify(this.os)); // 记录下初始状态
        this.python = this.processData(data.python);
        this.pythoninit = JSON.parse(JSON.stringify(this.python)); // 记录下初始状态
        this.testType = this.processData(data.type);
        this.testTypeinit = JSON.parse(JSON.stringify(this.testType)); // 记录下初始状态
        // 将选中的第一个复制给searchinit
        this.getSearchInit();
        this.search = JSON.parse(JSON.stringify(this.searchinit));
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
    getSearchInit() {
      // 将初始化的选中
      this.searchinit = {
        name: '',
        value: '',
        type: this.testTypeinit[0].desc,
        branch: this.branchinit[0].desc,
        cuda: this.cudainit[0].desc,
        os: this.osinit[0].desc,
        python: this.pythoninit[0].desc
      };
    },
    changeTagStatus(item, key) {
      let tmp_key = key;
      if (tmp_key === 'testType') {
        tmp_key = 'type';
      }
      item.checked = true;
      // 将选中以外的设置成false
      for (let i = 0; i < this[key].length; i++) {
        let id = this[key][i].id;
        if (parseInt(id, 10) !== parseInt(item.id, 10)) {
          this[key][i].checked = false;
        } else {
          this[key][i].checked = true;
          this.search[tmp_key] = this[key][i].desc;
        }
      }
    },
    processData(originData) {
      let tmp = [];
      for (let i = 0; i < originData.length; i++) {
        if (i === 0) {
          tmp.push({
            id: i,
            checked: true,
            desc: originData[i]
          });
        } else {
          tmp.push(
            {
              id: i,
              checked: false,
              desc: originData[i]
            }
          );
        }
      }
      return tmp;
    },
    async createJob() {
      this.content = []; // 初始化一下
      this.SelectChange(this.toData);
      let params = {
        name: this.search.name,
        type: this.search.type,
        value: this.search.value,
        python: this.search.python,
        cuda: this.search.cuda,
        os: this.search.os,
        branch: this.search.branch,
        mission: JSON.stringify(this.content)
      };
      const {code, data, message} = await api.post(FrameWorkJobUrl, params);
      if (parseInt(code, 10) === 200) {
        // 通知父组件更新视图
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
.form-pane-sty{
  width: 50%;
  align: center;
}
.demo-tree {
  width: 100%;
  line-height: 2;
}
.center-card-s {
  width: 98%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 600px;
  overflow: auto;
  font-size: 15px;
  color:lightslategrey
}
.new-card-s {
  width: 98%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 800px;
  overflow: auto;
  font-size: 15px;
  color:lightslategrey
}
.main {
  color:lightslategrey;
  margin-left: 2%;
  margin-top: 1%;
  margin-bottom: 1%;
  font-size: 20px;
  align: center;
}
.ivu-form-item{
  margin-bottom: 12px;
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
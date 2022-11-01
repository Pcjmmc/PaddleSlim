<template>
  <div>
    <Card class="center-card-s">
      <div>
        <p align="left"> 环境配置 </p>
      </div>
      <div style="margin-top: 1%;" v-if="os.length > 0">
        <span>
         系统:
          <span v-for="item, index in os">
            <span v-if="item.checked">
              <Tag
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'os')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
            <span v-else>
              <Tag
                checkable
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'os')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
          </span>
        </span>
      </div>
      <div style="margin-top: 1%;" v-if="search.type == 'pr' && branch.length > 0">
        <span>
         分支:
          <span v-for="item, index in branch">
            <span v-if="item.checked">
              <Tag
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'branch')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
            <span v-else>
              <Tag
                checkable
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'branch')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
          </span>
        </span>
      </div>
      <div style="margin-top: 1%;" v-if="cuda.length > 0">
        <span>
         CUDA:
          <span v-for="item, index in cuda">
            <span v-if="item.checked">
              <Tag
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'cuda')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
            <span v-else>
              <Tag
                checkable
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'cuda')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
          </span>
        </span>
      </div>
      <div style="margin-top: 1%;" v-if="python.length > 0">
        <span>
         python:
          <span v-for="item, index in python">
            <span v-if="item.checked">
              <Tag
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'python')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
            <span v-else>
              <Tag
                checkable
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'python')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
          </span>
        </span>
      </div>
      <div style="margin-top: 1%;" v-if="testType.length > 0">
        <span>
         类型:
          <span v-for="item, index in testType">
            <span v-if="item.checked">
              <Tag
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'testType')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
            <span v-else>
              <Tag
                checkable
                :checked="item.checked" 
                color="primary"
                @on-change="changeTagStatus(item, 'testType')"
              >
                <font size="3"> {{ item.desc }}</font>
              </Tag>
            </span>
          </span>
        </span>
      </div>
      <div style="margin-top: 1%;" v-if="testType.length > 0">
        <Form ref="addForm" :model="search" :rules="addRules">
          <FormItem prop="value"
          >
            取值:
            <Input
              v-model="search.value"
              placeholder="输入pr、commit、version或者wheel包"
              style="width:40%"
            ></Input>
          </FormItem>
        </Form>
      </div>
    </Card>
    <!--
    <div slot="right" class="main">
      <Tree
        ref="tree"
        :data="data2"
        show-checkbox multiple
        :render="renderContent"
        v-on:on-check-change="SelectChange"
      ></Tree>
    </div>
    -->
    <Card class="center-card-s">
      <div align="center" style="margin-top: 1%;">
        <tree-transfer
          ref="transfer"
          :title="title"
          :from_data='data2'
          :to_data='toData'
          :defaultProps="{label:'label'}"
          @add-btn='add'
          @remove-btn='remove'
          mode='transfer'
          height='490px'
          width='90%'
          openAll
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
            {
              pid: '1',
              id: '1-3',
              label: 'IO相关测试',
              key: 'io_function'
            },
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
              label: '动转静API单独组网测试',
              key: 'jit_api_function'
            },
            {
              pid: '2',
              id: '2-2',
              label: '动转静模型子结构测试',
              key: 'jit_models_function'
            }
          ]
        },
        {
          id: '3',
          label: 'API性能测试',
          key: 'api_benchmark'
        },
        {
          id: '4',
          label: '模型测试',
          key: 'models',
          children: [
            {
              pid: '4',
              id: '4-1',
              label: '图像识别',
              key: 'paddleclas'
            }
          ]
        },
        {
          id: '5',
          label: '模型性能测试',
          key: 'models_benchmark'
        },
        {
          id: '6',
          label: '预测部署',
          key: 'infer'
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
    treeTransfer
  },
  computed: {
  },
  methods: {
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
      this.python =  JSON.parse(JSON.stringify(this.pythoninit)); // 记录下初始状态
      this.testType =  JSON.parse(JSON.stringify(this.testTypeinit)); // 记录下初始状态
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
        if (parseInt(id) != parseInt(item.id)) {
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
        if (i == 0) {
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
      for (let idx = 0; idx < this.toData.length; idx++) {
        let item = this.toData[idx];
        if (item.children && item.children.length > 0) {
          item.children.forEach(element => this.content.push(element.key));
        } else {
          this.content.push(item.key);
        }
      }
      let params = {
        type: this.search.type,
        value: this.search.value,
        python: this.search.python,
        cuda: this.search.cuda,
        os: this.search.os,
        branch: this.search.type === 'pr' ? this.search.branch : null,
        mission: JSON.stringify(this.content)
      };
      const {code, data, message} = await api.post(FrameWorkJobUrl, params);
      if (parseInt(code, 10) === 200) {
        this.jobid = data.jid;
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
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 600px;
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
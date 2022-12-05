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
        <div v-if="os.length > 0" style="cursor:pointer;">
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
        <div style="margin-top: 1%;cursor:pointer;" v-if="branch.length > 0">
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
        <div style="margin-top: 1%;cursor:pointer;" v-if="cuda.length > 0">
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
        <div style="margin-top: 1%;cursor:pointer;" v-if="python.length > 0">
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
        <div style="margin-top: 1%;cursor:pointer;" v-if="testType.length > 0">
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
          :render-content-left="renderFunc"
          :render-content-right="renderFunc"
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
import { FrameWorkConfigUrl, FrameWorkJobUrl, FrameModuleConfigUrl } from '../../api/url.js';

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
      originData: []
    };
  },
  watch: {
  },
  mounted: async function () {
    await this.getModuleConfig();
    this.initData();
    await this.getSelectDatas();
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
    renderFunc(h, option) {
      let ret = [];
      if (option.data.desc) {
        ret.push(
          h('Tooltip', {
            props: {
              placement: 'right',
              transfer: true
            }
          }, [
            h('div', {
              style: {
                overflow: 'hidden',
                whiteSpace: 'nowrap',
                textOverflow: 'ellipsis'
              }
            }, option.data.label),
            h('span', {
              slot: 'content',
              style: {
                whiteSpace: 'normal',
                wordBreak: 'break-all'
              }
            }, option.data.desc)
          ])
        );
      } else {
        ret.push(
          h('div', {
            style: {
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              textOverflow: 'ellipsis'
            }
          }, option.data.label)
        );
      }
      return h(
        'div',
        {
          style: {
            align: 'center'
          }
        },
        ret
      );
    },
    async handleSubmit() {
      this.$refs.addForm.validate(async (valid) => {
        if (valid) {
          await this.createJob();
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
    async getModuleConfig() {
      const {code, data, message} = await api.get(FrameModuleConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.originData = JSON.parse(data.module_list);
      } else {
        this.originData = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async getSelectDatas() {
      const {code, data, message} = await api.get(FrameWorkConfigUrl);
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
          content: '请求出错: ' + message,
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
      if (this.content.length === 0) {
        this.$Message.error({
          content: '至少选择一个测试项目！',
          duration: 30,
          closable: true
        });
      } else {
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
          // 通知父组件更新视图, 父组件这里需要统一这些函数，可以什么也不做
          this.$emit('SubmitRequirement', data.jid);
          this.$emit('closeModal', false);
          this.$emit('searchByfilter');
          this.initData();
        } else {
          this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
          });
        }
      }
    }
  }
};
</script>

<style scoped>
.center-card-s {
  width: 98%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 600px;
  overflow: auto;
  font-size: 14px;
  color:lightslategrey
}
.new-card-s {
  width: 98%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 1000px;
  overflow: auto;
  font-size: 14px;
  color:lightslategrey
}
.ivu-form-item{
  margin-bottom: 12px;
  font-size: 14px;
}
</style>

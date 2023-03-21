<template>
  <div>
    <Card class="card-s-new">
      <div class="main">
        <p align="left" style="font-size:14px;font-weight:bold;"> 编译选项 </p>
      </div>
      <div>
        <Form
          ref="addForm"
          :model="search"
          :rules="addRules"
          :label-width="75"
          style="width: 85%"
        >
          <Row>
            <Col span="8">
             <FormItem label="系统:" prop="os">
                <Select clearable v-model="search.os">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in os"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="8">
              <FormItem
                label="分支:"
                prop="branch"
                :rules="{ required: true, message: '请选择分支', trigger: 'blur' }"
              >
                <Select clearable v-model="search.branch">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in branch"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
            <Col span="8">
              <FormItem label="CUDA:" prop="cuda">
                <Select clearable v-model="search.cuda">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in cuda"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
          </Row>
          <Row>
            <Col span="8">
              <FormItem label="Python:" prop="python">
                <Select clearable v-model="search.python">
                  <Option
                    :key="index"
                    :value="item"
                    v-for="(item, index) in python"
                  >{{ item }}</Option>
                </Select>
              </FormItem>
            </Col>
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
            <Col span="8">
              <FormItem label="取值:" prop="value">
                <Input
                  clearable
                  v-model="search.value"
                  placeholder="输入 pr、commit 或 包地址"/>
              </FormItem>
            </Col>
          </Row>
          <Row>
          <Col span="4">
            <FormItem label="预测库:" prop="OpenInfer">
              <i-switch v-model="search.OpenInfer">
                <span slot="open">开</span>
                <span slot="close">关</span>
              </i-switch>
            </FormItem>
          </Col>
          <Col span="4">
            <FormItem label="开启缓存:" prop="OpenCache">
              <i-switch v-model="search.OpenCache">
                <span slot="open">开</span>
                <span slot="close">关</span>
              </i-switch>
            </FormItem>
          </Col>
        </Row>
        </Form>
      </div>
      <Row
        type="flex"
        justify="center"
      >
        <Col span="4">
          <Button class="btn-success" @click="handleSummit">创建编译任务</Button>
        </Col>
        <Col span="4">
          <Button class="btn-success" @click="handleReset">重置</Button>
        </Col>
      </Row>
    </Card>
    <div style="margin-top: 2%;">
      <div v-for="item, index in content">
        <Card class="center-card-s">
          <Row>
            <span style="display:inline-block;width:100%;margin-right:1%;">
              <span style="float:left;">
                <a href="javascript:void(0)" @click="openXly(item.info)">
                  状态:<Icon type="md-open"></Icon>
                </a>
                <Button
                  type="error"
                  v-if="item.status=='error'"
                  style="width: 120px;"
                  @click="openXly(item.info)"
                >{{ item.status }}
                </Button>
                <Button
                  type="success"
                  v-else-if="item.status=='done'"
                  style="width: 120px;"
                  @click="openXly(item.info)"
                >{{ item.status }}
                </Button>
                <Button
                  type="warning"
                  v-else
                  style="width: 120px;"
                  @click="openXly(item.info)"
                >{{ item.status }}
                </Button>
                <span v-if="item.status=='error'"><font color="red">{{ item.result }}</font></span>
                系统: {{ getValue(item.env, "os") }}
                <span v-if="getValue(item.env, 'branch')">
                  | 分支: {{ getValue(item.env, "branch") }}
                </span>
              </span>
              <span style="float:right;">创建时间: {{ item.create_time }}</span>
            </span>
          </Row>
          <Row style="margin-top: 1%;">
            <span style="display:inline-block;width:100%;margin-right:1%;">
              <span style="float:left;"> {{ getDisplay(item.env) }}</span>
              <span style="float:right;">
              <!--
                <el-popconfirm title="确定取消？">
                  <el-button
                    slot="reference"
                    :disabled="item.status!=='running'"
                    size="mini"
                    type="primary"
                    icon="el-icon-video-pause"
                    circle
                  ></el-button>
                </el-popconfirm>
                <el-popconfirm title="确定重跑？">
                  <el-button
                    slot="reference"
                    :disabled="item.status ==='running'"
                    size="mini"
                    type="warning"
                    icon="el-icon-refresh-right"
                    circle
                  ></el-button>
                </el-popconfirm>
              -->
                <el-popconfirm title="确定删除？" @confirm="deleteJob(item, index)">
                  <el-button
                    slot="reference"
                    size="mini"
                    type="danger"
                    icon="el-icon-delete"
                    circle
                  ></el-button>
                </el-popconfirm>
              </span>
            </span>
          </Row>
          <Row>
            <span>产物地址: <a :href="item.wheel">{{ item.wheel }}</a>
              <Icon
                class="ivu-icon ivu-icon-ios-copy-outline copyBtn"
                type="ios-copy-outline"
                color="green"
                size="15"
                @click="copyData(item.wheel)"
              ></Icon>
            </span>
          </Row>
        </Card>
      </div>
      <Page
        :total="total"
        :current="parseInt(page)"
        :page-size="parseInt(pagesize)"
        size="small"
        style="text-align: center;"
        v-on:on-change="pageChange"
        >
      </Page>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { FrameWorkConfigUrl, FrameCompileSearchUrl, FrameCompileCreateUrl, FrameWorkDelComUrl } from '../../api/url.js';
import Clipboard from 'clipboard';
import api from '../../api/index';

export default {
  name: 'CompileService',
  data: function () {
    return {
      total: 0,
      page: 1,
      pagesize: 15,
      content: [
      ],
      search: {
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: '',
        OpenInfer: false,
        OpenCache: false
      },
      addRules: {
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
      branch: [
      ],
      cuda: [
      ],
      os: [
      ],
      python: [
      ],
      testType: [
      ]
    };
  },
  watch: {
  },
  mounted: async function () {
    this.initData();
    await this.getSelectDatas();
    await this.getData();
  },
  components: {
  },
  computed: {
  },
  methods: {
    handleReset() {
      this.initData();
    },
    copyData(url) {
      let clipboard = new Clipboard('.copyBtn', {
          text: function (trigger) {
            clipboard.destroy();
            return url;
          }
      });
      clipboard.on('success', e => {
        this.$Message.success('复制成功~');
        e.clearSelection();
      });
      clipboard.on('error', e => {
        this.$Message.error('复制失败,请手动复制~');
      });
    },
    getValue(env, key) {
      let tmp_env = JSON.parse(env);
      return tmp_env[key];
    },
    getDisplay(item) {
      let env = JSON.parse(item);
      let content_list = [];
      let key_list = ['value', 'python', 'cuda'];
      for (let i = 0; i <= key_list.length; i++) {
        let key = key_list[i];
        if (env[key]) {
          if (key === 'value') {
            let con = env.type + ':' + env[key];
            content_list.push(con);
          } else {
            content_list.push(env[key]);
          }
        }
      }
      content_list.push('Wheel安装包');
      return content_list.join(' | ');
    },
    openXly(url) {
      if (url) {
        window.open(url, '_blank');
      } else {
        this.$Message.info({
          content: '下游任务没有回写任务地址!',
          duration: 5,
          closable: true
        });
      }
    },
    async getSelectDatas() {
      const {code, data, message} = await api.get(FrameWorkConfigUrl);
      if (parseInt(code, 10) === 200) {
        this.branch = data.compile_branch;
        this.cuda = data.compile_cuda;
        this.os = data.compile_os;
        this.python = data.compile_python;
        this.testType = data.compile_type;
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
    async pageChange(pageNum) {
      this.page = pageNum;
      await this.getData();
    },
    async getData() {
      this.content = [];
      let params = {
        uid: Cookies.get('userid'),
        page_index: this.page,
        limit: this.pagesize
      };
      const {code, data, message, all_count} = await api.get(FrameCompileSearchUrl, params);
      if (parseInt(code, 10) === 200) {
        this.content = data;
        this.total = all_count;
      } else {
        this.content = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    initData() {
      this.search = {
        type: '',
        value: '',
        branch: '',
        cuda: '',
        os: '',
        python: '',
        OpenInfer: false,
        OpenCache: true
      };
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
      // 防止有人选了pr，选了分支，又修改了其他值
      let params = {
        type: this.search.type,
        value: this.search.value,
        python: this.search.python,
        cuda: this.search.cuda,
        os: this.search.os,
        branch: this.search.branch,
        dist_type: Boolean(this.search.OpenInfer),
        cache: Boolean(this.search.OpenCache)
      };
      const {code, message} = await api.post(FrameCompileCreateUrl, params);
      if (parseInt(code, 10) === 200) {
        // 立马刷新
        this.initData();
        await this.getData();
      } else {
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    async deleteJob(item, index) {
      // 删除选项
      let params = {
        id: item.id
      };
      const {code, message} = await api.post(FrameWorkDelComUrl, params);
      if (parseInt(code, 10) === 200) {
        // 从content中将index删除 todo
        this.content.splice(index, 1);
        this.$Message.info({
          content: '删除成功',
          duration: 2,
          closable: true
        });
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
.center-card-s {
  width: 100%;
  font-size: 14px;
  border-color: green;
  color: lightslategrey
}
.card-s-new {
  width: 100%;
  font-size: 14px;
  color: lightslategrey
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.ul_box {
  width: 600px;
  height: 60px;
  display: inline-block;
  margin: 20px 2px;
  overflow: hidden;
}
.my_timeline_item {
  display: inline-block;
  width: 100px;
}
.my_timeline_node {
  width:10px;
  height: 10px;
  font-size: 18;
  box-sizing: border-box;
  border-radius: 50%;
}
.my_timeline_item_line {
  width: 90px;
  height: 10px;
  margin: -6px 0 0 10px;
  border-top: 2px solid #E4E7ED;
  border-left: none;
}
.my_timeline_item_content {
  margin: 10px 0 0 -10px;
  display: flex;
  flex-flow: column;
  cursor: pointer;
}
</style>

<template>
  <div>
    <Card class="card-s-new">
      <div class="main">
        <p align="left"> 编译选项 </p>
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
            <Col span="6">
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
            <Col span="6">
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
            <Col span="4">
              <FormItem label="预测库:" prop="OpenInfer">
                <i-switch v-model="search.OpenInfer">
                  <span slot="open">开</span>
                  <span slot="close">关</span>
                </i-switch>
              </FormItem>
            </Col>
            <Col>
              <FormItem label="开启缓存:" prop="OpenCache">
                <i-switch v-model="search.OpenCache">
                  <span slot="open">开</span>
                  <span slot="close">关</span>
                </i-switch>
              </FormItem>
            </Col>
          </Row>
          <Row>
            <Col span="6">
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
          </Row>
          <Row>
            <Col span="6">
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
                <Input v-model="search.value" placeholder="输入 pr、commit 或 包地址"/>
              </FormItem>
            </Col>
          </Row>
        </Form>
      </div>
      <Row
        type="flex"
        justify="center"
        style="margin-top: 1%;"
      >
        <Col span="4">
          <Button type="primary" @click="handleSummit">创建编译任务</Button>
        </Col>
        <Col span="4">
          <Button type="primary" @click="handleReset">重置</Button>
        </Col>
      </Row>
    </Card>
    <div style="margin-top: 2%;">
      <div v-for="item, index in content">
        <Card class="center-card-s">
          <Row>
            <span style="display:inline-block;width:95%;margin-right:2%;">

              <span style="float:left;">
                  <Button
                    type="error"
                    v-if="item.status=='error'"
                    style="width: 120px;"
                  >状态: {{ item.status }}
                  </Button>
                  <Button
                    type="success"
                    v-else-if="item.status=='done'"
                    style="width: 120px;"
                  >状态: {{ item.status }}
                  </Button>
                  <Button
                  type="warning"
                  v-else="item.status=='error'"
                  style="width: 120px;"
                >状态: {{ item.status }}
                </Button>
                系统: {{ getValue(item.env, "os") }}
                <span v-if="getValue(item.env, 'branch')">
                  | 分支: {{ getValue(item.env, "branch") }}
                </span>
              </span>
              <span style="float:right;">创建时间: {{ item.create_time }}</span>
            </span>
          </Row>
          <Row style="margin-top: 1%;">
            <span style="display:inline-block;width:95%;margin-right:2%;">
              <span> {{ getDisplay(item.env) }}</span>
            </span>
          </Row>
          <Row style="margin-top: 1%;">
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
import { FrameWorkConfigUrl, FrameCompileSearchUrl, FrameCompileCreateUrl } from '../../api/url.js';
import Clipboard from 'clipboard';
import api from '../../api/index';

export default {
  name: 'CompileService',
  data: function () {
    return {
      total: 0,
      page: 1,
      pagesize: 10,
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
  mounted: function () {
    this.initData();
    this.getSelectDatas();
    this.getData();
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
    async getSelectDatas() {
      const {code, data, msg} = await api.get(FrameWorkConfigUrl);
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
          content: '请求出错: ' + msg,
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
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  max-height: 600px;
  overflow: auto;
  font-size: 15px;
  color: lightslategrey
}
.card-s-new {
  width: 96%;
  margin-left: 2%;
  margin-right: 2%;
  font-size: 15px;
  color: lightslategrey
}
.main {
  color:lightslategrey;
  margin-left: 1%;
  margin-bottom: 2%;
  font-size: 18px;
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
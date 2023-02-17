<template>
  <div>
    <div style="height:30px;">
      <div style="float: left;">
        <el-dropdown>
          <span class="el-dropdown-link ins">
            模块快速索引<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <div v-for="(item, index) in allData" :key="index">
              <a @click="changeModuel(item.id)" ><el-dropdown-item>{{item.id}}.{{item.module}}</el-dropdown-item></a>
            </div>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <div style="float: right;">
        <Button
          class="btn-success"
          @click="exportReport"
        >查看报告</Button>
      </div>
    </div>
    <div v-for="(item, index) in allData" :key="index">
      <base-result
        :idx="index"
        :moduleid="item.id"
        :date="item.create_time"
        :modulename="item.module"
        :owner="item.owner"
        :risk="item.risk"
        :regression="item.regression"
        @searchByfilter="searchByfilter"
      ></base-result>
    </div>
    <!--
    <div>
      <Modal
        width="90%"
        v-model="showData"
        title="结论详情"
        v-on:on-cancel="cancelShowData"
      >
      
      <SummaryResult> </SummaryResult>
      <Card>
        <p slot="title" style="text-align:center">整体进展</p>
        <p>
          <Table
            border
            :columns="summaryColumns"
            :data="summaryData"
            >
          </Table>
        </p>
      </Card>
        <div v-for="(item, key, index) in detailData" :key="index">
          <Card style="margin-top: 1%;">
            <p slot="title" style="text-align:center">{{ key }}</p>
            <p>
              <Table
                border
                :columns="detailColumns"
                :data="item"
              >
              </Table>
            </p>
          </Card>
        </div>
        <div slot="footer">
          <Button type="primary" @click="saveData">保存</Button>
          <Button type="primary" @click="sendEmail">发邮件</Button>
        </div>
      </Modal>
    </div>
    -->
  </div>
</template>

<script>

import BaseResult from './BaseResult.vue';
import api from '../../api/index';
import { dateFmt } from '../../util/help.js';
import { SearchNewConclusionUrl } from '../../api/url.js';

export default {
  name: 'NewConclusion',
  data: function () {
    return {
      allData: [],
      showData: false,
      detailColumns: [
        {
          title: '问题详情',
          align: 'center',
          key: 'data'
        },
        {
          title: '严重程度',
          align: 'center',
          key: 'rate'
        },
        {
          title: '是否影响发版',
          align: 'center',
          key: 'affect_release'
        },
        {
          title: '负责人',
          align: 'center',
          key: 'rd'
        }
      ],
      // summaryData: [],
      summaryColumns: [
        {
          title: '方向',
          align: 'center',
          key: 'direction'
        },
        {
          title: '进展',
          align: 'center',
          key: 'progress'
        },
        {
          title: '遗留风险数据',
          align: 'center',
          key: 'risknum'
        },
        {
          title: '影响发版风险数',
          align: 'center',
          key: 'affect_num'
        }
      ]
    };
  },
  watch: {
    versionName: function () {
      this.getData();
    }
  },
  components: {
    BaseResult
  },
  mounted: async function () {
    await this.getData();
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version ? this.$store.state.version : this.$route.params.version;
      }
    },
    summaryData() {
      let menuItemArr = [];
      for (var i = 0; i < this.allData.length; i++) {
        let affect_num = 0;
        for (var j = 0; j < this.allData[i].risk.length; j++) {
          if (this.allData[i].risk[j].important === '是') {
            affect_num += 1;
          }
        }
        let tmp = {
          direction: this.allData[i].modulename,
          progress: this.allData[i].conclusion,
          risknum: this.allData[i].risk.length,
          affect_num: affect_num
        };
        menuItemArr.push(tmp);
      }
      return menuItemArr;
    },
    detailData() {
      // 计算这个
      let menuItemArr = {};
      for (var i = 0; i < this.allData.length; i++) {
        let key = this.allData[i].modulename;
        let problem = this.allData[i].risk;
        menuItemArr[key] = problem;
      }
      return menuItemArr;
    }
  },
  methods: {
    exportReport() {
      // 将关键数据按照一定的样式导出
      const { href } = this.$router.resolve({name: 'SummaryResult'});
      window.open(href, '_blank');
    },
    async sendEmail() {
      // 提交数据，这里应该支持的的是发邮件和导出
      this.showData = false;
    },
    async saveData() {
      // 保存数据
      this.showData = false;
    },
    changeModuel(idName) {
      document.getElementById(idName).scrollIntoView(true)
    },
    cancelShowData() {
      this.showData = false;
    },
    async searchByfilter() {
      await this.getData();
    },
    async getData() {
      const {code, data, message} = await api.get(SearchNewConclusionUrl);
      if (parseInt(code, 10) === 200) {
        this.allData = this.RestructData(data);
        console.log('this all Data', this.allData);
      } else {
        this.allData = [];
        this.$Message.error({
          content: '请求出错: ' + message,
          duration: 30,
          closable: true
        });
      }
    },
    RestructData(data) {
      let settings = data.settings;
      let content = data.content;
      for (var i = 0; i < settings.length; i++) {
          settings[i].risk = [];
          settings[i].regression = {
            round: 0,
            total: 0,
            pass: 0,
            fail: 0,
            running: 0
          };
          settings[i].create_time = dateFmt(new Date(), 'yyyy-MM-dd hh:mm:ss');
        for (var j = 0; j < content.length; j++) {
          if (settings[i].id === content[j].module_id) {
            // 将数据解析出来，拼装到settings
            let detail = JSON.parse(content[j].content);
            console.log('detail is', detail);
            settings[i].risk = detail.risk;
            settings[i].regression = detail.regression;
            settings[i].create_time = content[j].create_time;
          }
        }
      }
      return settings;
    }
  }
};
</script>

<style scoped>
.center-card-s {
  width: 100%;
  max-height: 600px;
  overflow: auto;
  margin-bottom: 1%
}
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size:14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
.el-icon-arrow-down {
  font-size: 12px;
}
.ins {
  font-size: 18px;
}
</style>


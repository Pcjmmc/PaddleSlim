<template>
  <div class="all-line-row">
    <!--
    <div style="text-align:right;">
      <Button
        class="btn-success"
        @click="previewReport"
      >预览</Button>
    </div>
    -->
    <div id="app" ref="document" style="margin-top:0.2%;">
      <h1 slot="title" style="text-align:center">集测风险&进展</h1>

      <Card
        v-if="JSON.stringify(important_summary) !== '{}' || JSON.stringify(important) !== '{}'" class="main-card"
      >
        <h2 slot="title" style="text-align:center; color: #F56C6C;">重点关注高风险</h2>
        <div style="font-size: 14px;margin-left: 1%;" v-if="JSON.stringify(important_summary) !== '{}'">
          <Table :columns="columns" :data="important_summary"></Table>
        </div>
        <div v-for="(item, key, index) in important" v-if="JSON.stringify(important) !== '{}'">
          <div style="margin-top: 1%;" :bordered="false">
            <Card>
              <h3 slot="title" style="text-align:left;  color: #F56C6C;">{{ key }}</h3>
              <ol>
                <div v-for="(itm, idx) in item">
                  <Row>
                    <Col span="22" offset="1">
                        <li>【{{itm.type}}】 {{itm.content}}。{{itm.influence}}。 PR：<a :href="itm.pr">{{itm.pr}}</a> 负责人：@{{itm.owner}}</li>
                    </Col>
                  </Row>
                  <!-- <summary-base :idx="idx" :datas="itm"></summary-base> -->
                </div>
              </ol>
            </Card>
        </div>
        </div>
      </Card>
      <Card
        v-if="JSON.stringify(regression_summary) !== '{}' || regression.length > 0"
        style="margin-top: 1%;"  class="main-card"
      >
        <h2 slot="title" style="text-align:center">集成测试情况</h2>
        <div v-if="regression.length > 0" style="margin-top: 1%;">
          <progress-base :datas="regression"> </progress-base>
        </div>
      </Card>
      <Card
        v-if="JSON.stringify(icafes) !== '{}'"
        style="margin-top: 1%;"  class="main-card"
      >
        <h2 slot="title" style="text-align:center">各方向详细进展</h2>
        <div style="margin-top: 1%;">
          <detail-base :settings="settings" :content="content"></detail-base>
        </div>
      </Card>
      <Card
        v-if="JSON.stringify(icafes) !== '{}'"
        style="margin-top: 1%;"  class="main-card"
      >
        <h2 slot="title" style="text-align:center">卡片汇总</h2>
        <div style="margin-top: 1%;">
          <card-base :icafes="icafes"> </card-base>
        </div>
      </Card>
    </div>
    <Modal
      v-model="ShowPreview"
      width="900px"
      v-on:on-cancel="handleReset"
    >
      <div id="previewApp" ref="document" style="margin-top:0.2%;">
        <Card
          v-if="JSON.stringify(important_summary) !== '{}' || JSON.stringify(important) !== '{}'"
        >
          <p slot="title" style="text-align:center">重点关注高风险</p>
          <div style="font-size: 14px;margin-left: 1%;" v-if="JSON.stringify(important_summary) !== '{}'">
            <Table :columns="columns" :data="important_summary"></Table>
          </div>
          <div v-for="(item, key, index) in important" v-if="JSON.stringify(important) !== '{}'">
            <div style="margin-top: 1%;" :bordered="false">
              <h3 slot="title" style="text-align:center;">{{ key }}</h3>
              <div v-for="(itm, idx) in item">
                <summary-base :idx="idx" :datas="itm"></summary-base>
              </div>
          </div>
          </div>
        </Card>
        <Card
          v-if="JSON.stringify(regression_summary) !== '{}' || regression.length > 0"
          style="margin-top: 1%;"
        >
          <p slot="title" style="text-align:center">集成测试情况</p>
          <div v-if="regression.length > 0" style="margin-top: 1%;">
            <progress-base :datas="regression"> </progress-base>
          </div>
        </Card>
        <Card
          v-if="JSON.stringify(icafes) !== '{}'"
          style="margin-top: 1%;"
        >
          <p slot="title" style="text-align:center">各方向详细进展</p>
          <div style="margin-top: 1%;">
            <detail-base :settings="settings" :content="content"></detail-base>
          </div>
        </Card>
        <Card
          v-if="JSON.stringify(icafes) !== '{}'"
          style="margin-top: 1%;"
        >
          <p slot="title" style="text-align:center">卡片汇总</p>
          <div style="margin-top: 1%;">
            <card-base :icafes="icafes"> </card-base>
          </div>
        </Card>
      </div>
      <div slot="footer">
        <Button type="text" @click="handleReset">取消</Button>
        <Button type="primary" @click="exportReport">下载</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { SearchSummaryConclusionUrl } from '../../api/url.js';
import api from '../../api/index';
import SummaryBase from './SummaryBase.vue';
import ProgressBase from './ProgressBase.vue';
import CardBase from './CardBase.vue';
import DetailBase from './DetailBase.vue';

export default {
  name: "SummaryResult",
  data: function () {
    return {
      ShowPreview: false,
      settings: [],
      important: {},
      regression: [],
      content: [],
      icafes: {},
      important_summary: [],
      regression_summary: {},
       columns: [
        {
          title: '总量',
          align: 'center',
          key: '总量'
        },
        {
          title: '已解决',
          align: 'center',
          key: '已解决'
        },
        {
          title: '未解决',
          align: 'center',
          key: '未解决'
        },
        {
          title: '延期',
          align: 'center',
          key: '延期'
        },
        {
          title: '修复率',
          align: 'center',
          key: '修复率'
        }
      ]
    };
  },
  watch: {
    versionName: async function () {
      this.$router.push({
        name: 'SummaryResult',
        params: {
          version: this.versionName
        }
      }).catch(error => {
        if (error.name !== 'NavigationDuplicated') {
          throw error;
        }
      });
      await this.getData();
    },
    $route() {
      let _version = this.$route.params.version;
      Cookies.set('version', _version);
      Cookies.set('ver', _version);
      this.$store.commit('changeVersion', _version);
    }
  },
  components: {
    SummaryBase,
    ProgressBase,
    CardBase,
    DetailBase
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version ? this.$store.state.version : this.$route.params.version;
      }
    }
  },
  mounted: async function () {
    await this.getData();
  },
  methods: {
    previewReport() {
      this.ShowPreview = true;
    },
    handleReset() {
      this.ShowPreview = false;
    },
    // exportReport() {
    //   let doc = document.getElementById('previewApp');
    //   var opt = {
    //     margin: 1,
    //     filename: 'Report.pdf',
    //     image: { type: 'jpeg', quality: 0.98 },
    //     html2canvas: { scale: 4 }
    //   };
    //   html2pdf().from(doc).set(opt).save();
    // },
    changeObjtoArry(data) {
      let result = [];
      for (let item in data) {
        let tmp = data[item];
        tmp['step'] = item;
        result.push(tmp);
      }
      return result;
    },
    async getData() {
      const {code, data, message} = await api.get(SearchSummaryConclusionUrl);
      if (parseInt(code, 10) === 200) {
        this.settings = data.settings;
        this.important = data.important;
        this.important_summary = [data.important_summary];
        this.regression_summary = data.regression_summary;
        this.regression = this.changeObjtoArry(data.regression);
        if (JSON.stringify(this.regression_summary) !== '{}') {
          this.regression_summary['step'] = '整体';
          this.regression.unshift(this.regression_summary);
        }
        this.content = data.content;
        this.icafes = data.icafes;
        this.important = {
          分布式: [
            {
              content: '这是风险1',
              influence: 'hshshs',
              level: 5,
              important: '是',
              status: '未解决',
              type: 'Bug',
              pr: 'hshsh',
              icafe: [
                {
                  url: 'xxxxxx',
                  owner: '张三',
                  title: '这是一个icafe卡片',
                  ref: 0
                },
                {
                  url: 'yyyyyy',
                  owner: '李四',
                  title: '这是一个icafe卡片',
                  ref: 0
                }
              ]
            },
            {
              content: '这是风险2',
              influence: 'lalala',
              level: 4,
              important: '是',
              status: '未解决',
              type: 'Delay',
              pr: 'hshsh',
              icafe: [
                {
                  url: 'yyyyyy',
                  owner: '王五',
                  title: '这是一个icafe卡片',
                  ref: 1
                }
              ]
            }
          ]
        }
        this.important = data.important;
      } else {
        this.settings = [];
        this.important = {};
        this.regression = [];
        this.important_summary = [];
        this.regression_summary = {};
        this.content = [];
        this.icafes = {};
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
.all-line-row {
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 1%;
  margin-right: 1%;
  font-size: 18px;
}
.ivu-form-item{
  margin-bottom: 12px;
  font-size: 14px;
}
.btn-success {
  color: #fff;
  background-color: #67c23a;
  border-color: #67c23a;
}
.main-card {
  border: 1px solid #809399;
  margin-bottom: 20px;
}
</style>

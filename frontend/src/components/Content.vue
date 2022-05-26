<template>
<div>
  <div style="margin-bottom: 1.5%">
    <!--
    <div v-if="allSteps.integration !== undefined && allSteps.integration.flag">
      <intergration
        :repoinfo="repoinfo"
        :bugdata="bugdata"
        :processdata="processdata"
      >
      </intergration>
    </div>
    <div v-else-if="allSteps.regression !== undefined && allSteps.regression.flag">
      <regression :data="bugdata"></regression>
    </div>
    <div v-else-if="allSteps.createtag !== undefined && allSteps.createtag.flag">
      <intergration
        :repoinfo="repoinfo"
        :bugdata="bugdata"
        :processdata="processdata"
      >
      </intergration>
    </div>
    <div v-else-if="allSteps.release !== undefined && allSteps.release.flag">
      <regression :data="bugdata"></regression>
    </div>
    !-->
    <div>
      <intergration
        :repoinfo="repoinfo"
        :bugdata="bugdata"
        :processdata="processdata"
        :summary="summary"
      >
      </intergration>
    </div>
  </div>
  <!--
  <div>
    <Modal v-model="allSteps.createtag !== undefined && allSteps.createtag.flag" title="快速打tag" @on-cancel="handleReset" width="600px">
        <Form ref="addForm" :model="tagForm" :label-width="80">
          <FormItem label="分支" prop="branch">
            <Input disabled v-model="tagForm.branch"/>
          </FormItem>
          <FormItem label="commit: " prop="commit">
            <Input v-model="tagForm.commit"/>
          </FormItem>
          <FormItem label="tag名称: " prop="tagName">
            <Input v-model="tagForm.tagName"/>
          </FormItem>
        </Form>
        <div slot="footer">
          <Button type="text" @click="handleReset">取消</Button>
          <Button type="primary" @click="handleSubmit">确定</Button>
        </div>
      </Modal>
  </div>
  -->
</div>
</template>

<script>
import Cookies from 'js-cookie';
import api from '../api/index';
import { ReleaseVersionUrl, BugUrl, DevelopVersionUrl } from '../api/url.js';
import BaseInfo from './BaseInfo.vue';
import { dateFmt } from '../util/help.js';
import Intergration from './Intergration.vue';
import Regression from './Regression.vue';

export default {
  data: function () {
    return {
      tagForm: {
        branch: '',
        tagName: '',
        commit: ''
      },
      repoinfo: {},
      processdata: {},
      summary: [],
      allSteps: {},
      // integrationdata: {
      //   data: []
      // },
      bugdata: []
    }
  },
  mounted: function () {
    this.initData();
    this.getData();
  },
  watch: {
    versionName: function () {
      this.getData();
    }
  },
  components: {
    BaseInfo,
    Intergration,
    Regression
  },
  computed: {
    versionName: {
      get() {
        return this.$store.state.version;
      }
    }
  },
  methods: {
    async getData() {
      // 判断参数如果参数中有tag，则name=version；如果没有，则name=release+version
      let tmpVersion = Cookies.get('version');
      let _params = {
        'version': tmpVersion,
        'appid': Cookies.get('appid')
      };
      let code = null;
      let data = null;
      let version = null;
      if (tmpVersion === 'develop') {
        let res = await api.get(DevelopVersionUrl, _params);
        code = res.code;
        data = res.data;
        version = res.version;
      } else {
        let res = await api.get(ReleaseVersionUrl, _params);
        code = res.code;
        data = res.data;
        version = res.version;
      }
      // 获取任务进展数据
      // 获取bug数据
      // console.log("code", code)
      if (parseInt(code) == 200) {
        this.repoinfo = data.repo_info;
        // this.allSteps = data.all_steps;
        this.tagForm.branch = this.repoinfo.branch;
        // this.integrationdata = data.integration_data;
        this.processdata = data.process_data;
        this.summary = data.summary;
      } else {
        this.repoinfo = {};
        // this.allSteps = {};
        this.$Message.error({
          content: '请求出错: ' + version,
          duration: 30,
          closable: true
        })
      }
      await this.getbugdata();
    },
    async getbugdata() {
      let _params = {'tag': this.repoinfo.tag};
      const {code, data, version} = await api.get(BugUrl, _params);
      if (parseInt(code, 10) === 200) {
        this.bugdata = data;
      } else {
        this.bugdata = [];
        this.$Message.error({
          content: '请求出错: ' + version,
          duration: 30,
          closable: true
        });
      }
    },
    async selectDate() {
      this.getData();
    },
    initDate() {
      let day1 = new Date();
      day1.setDate(day1.getDate() - 1);
      return day1;
    },
    initData() {
      this.tagForm.tagName = '';
      this.tagForm.commit = '';
    },
    handleReset(auto) {
      // this.allSteps.createtag.flag = false;
      this.initData(auto);
    },
    async handleSubmit(auto) {
      console.log('content of this tagForm is', this.tagForm);
      await this.getData();
      // 成功或失败，都需要关闭窗口
      this.initData(auto);
    },
    // showModal(key, item) {
    //   let status = item.status;
    //   if (status == 'wait') {
    //     this.$Message.info({
    //       content: "请先保证任务通过并修复卡片，请稍后再试。。。",
    //       duration: 3,
    //       closable: true
    //     });
    //   } else {
    //     for (let ky in this.allSteps) {
    //       this.allSteps[ky].flag = false;
    //     }
    //     if (key == 'createtag') {
    //       if (status == 'process') {
    //         this.allSteps[key].flag = true;
    //       }
    //     } else {
    //       this.allSteps[key].flag = true;
    //     }
    //   }
    // },
    jumper(row) {
      let _params = {
        'tid': row.tid,
        'tname': row.project_name,
        'build_type_id': row.build_type_id
      };
      _params = Object.assign(_params, row);
      // 打开新的页面展示详情
      const { href } = this.$router.resolve({name: row.task_type, query: _params});
      window.open(href, '_blank');
    }
  }
};
</script>

<style scoped>
.all-line-row {
  margin-bottom: 0.5%;
  margin-left: 0.5%;
}
.center-card-s {
    width: 100%;
    max-height: 600px;
    overflow:auto;
  }
</style>

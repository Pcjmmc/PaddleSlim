<template>
  <div>
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="单机模型统计"
        name="single"
      >
      </el-tab-pane>
      <el-tab-pane
        label="多机模型统计"
        name="muti"
      >
      </el-tab-pane>
      <el-tab-pane
        label="分布式模型统计"
        name="distributed"
      >
      </el-tab-pane>
      <model-statistics :datas="datas"></model-statistics>
    </el-tabs>
  </div>
</template>
<script>

import modelStatistics from './modelStatistics.vue';
import api from '../../../api/index';
import { ModelsBenchmarkHomeStatistics } from '../../../api/url.js';

export default {
  name: 'modelPage',
  data: function () {
    return {
      tabName: 'single',
      datas: []
    };
  },
  watch: {
  },
  mounted: function () {
    this.getData();
  },
  components: {
    modelStatistics
  },
  computed: {},
  methods: {
    async clickTab(name) {
      this.tabName = name.name;
      this.datas = [];
      await this.getData();
    },
    async getData() {
      // 根据参数获取单机/多机/分布式的数据
      let params = {
        field: this.tabName
      };
      const { code, data, message } = await api.post(ModelsBenchmarkHomeStatistics, params);
      if (parseInt(code, 10) === 200) {
         let paddle_res = this.changeData('paddle', data);
         let torch_res = this.changeData('pytorch', data);
         this.datas.push(paddle_res);
         this.datas.push(torch_res);
      } else {
        this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
        });
      }
    },
    changeData(type, data) {
      let result = [];
      let temp = [];
      temp = data[type] ? data[type] : [];
      for (var i = 0; i < temp.length; i++) {
        let repo_name = type;
        let tp_dt = {};
        for (let key in temp[i]) {
          if (temp[i].hasOwnProperty(key)) {
            tp_dt = temp[i][key];
            tp_dt.repo_name = repo_name + '_' + key;
          }
        }
        result.push(tp_dt);
      }
      return result;
    }
  }
};
</script>

<style scoped>
</style>
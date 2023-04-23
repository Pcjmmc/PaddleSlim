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
        name="multi"
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
      await this.getData();
    },
    async getData() {
      // 根据参数获取单机/多机/分布式的数据
      let params = {
        mode: this.tabName
      };
      console.log('request params is', params);
      this.datas = [
        {
          repo_name: 'paddle-class',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
         {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
         {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        },
        {
          repo_name: 'paddle-nlp',
          config_num: '150',
          model_num: '120'
        }
      ];
    }
  }
};
</script>

<style scoped>
</style>
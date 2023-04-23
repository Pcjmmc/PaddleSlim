<template>
  <div>
    <el-tabs
        v-model="tabName"
        type="card"
        @tab-click="clickTab"
    >
        <el-tab-pane
        label="动转静与动态图GSB"
        name="dySt"
        >
        </el-tab-pane>
        <el-tab-pane
        label="FP16与FP32GSB"
        name="fp"
        >
        </el-tab-pane>
        <compare-line
          id="main4"
          :option="option"
          :optionData="datas"
          :legend="legend"
        ></compare-line>
    </el-tabs>
  </div>
</template>
<script>

import compareLine from './compareLine.vue';

export default {
  name: 'compareSence',
  props: {
    search: {
      type: Object,
      default: function () {
        return {};
      }
    }
  },
  data: function () {
    return {
      tabName: 'dySt',
      datas: {},
      option: [],
      title: '',
      legend: []
    };
  },
  watch: {
  },
  mounted: function () {
    this.getDatas();
  },
  components: {
    compareLine
  },
  computed: {},
  methods: {
    async clickTab(name) {
      this.tabName = name.name;
      await this.getDatas();
    },
    async getDatas() {
      console.log('this.search', this.search);
      console.log(this.tabName);
      // 根据参数获取单机/多机/分布式的数据
      this.legend = ['G', 'S', 'B'];
      this.option = ['2022.02.02', '2022.02.03', '2022.02.04', '2022.02.05', '2022.02.06'];
      this.title = this.tabName;
      this.datas = {
        '2022.02.02': {'G': 10, 'S': 6, 'B': 4},
        '2022.02.03': {'G': 12, 'S': 8, 'B': 3},
        '2022.02.04': {'G': 5, 'S': 8, 'B': 9},
        '2022.02.05': {'G': 17, 'S': 21, 'B': 28},
        '2022.02.06': {'G': 13, 'S': 7, 'B': 16}
      };
    }
  }
};
</script>

<style scoped>
</style>
<template>
  <div>
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
        <el-tab-pane
        label="与pytorchGSB"
        name="other"
        >
        </el-tab-pane>
        <el-tab-pane
        label="与稳定版GSB"
        name="stable"
        >
        </el-tab-pane>
       <compare-line
        id="main3"
        :option="option"
        :optionData="datas"
        :legend="legend"
        ></compare-line>
    </el-tabs>
  </div>
</template>
<script>

import compareLine from './compareLine.vue';
import api from '../../../api/index';
import { dateFmt } from '../../../util/help.js';
import { ModelsBenchmarkHomeGBS } from '../../../api/url.js';

export default {
  name: 'compareProd',
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
      tabName: 'other',
      datas: {
      },
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
      let end_time = new Date(this.search.dt[1]);
      end_time = end_time.setDate(end_time.getDate() + 1);
      end_time = new Date(end_time);
      let params = {
        task_name: this.search.task_name,
        config_name: this.search.config_name,
        index_name: this.search.index_name,
        summary_type: this.search.summary_type,
        start_time: dateFmt(this.search.dt[0], 'yyyy-MM-dd'),
        end_time: dateFmt(end_time, 'yyyy-MM-dd'),
        tab_postion: 'up',
        vs_name: this.tabName
      };
      const { code, data, message } = await api.post(ModelsBenchmarkHomeGBS, params);
      if (parseInt(code, 10) === 200) {
        this.parseData(data);
      } else {
        this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
        });
      }
    },
    parseData(data) {
      let tmp_data = {};
      let tmp_option = [];
      // 根据参数获取单机/多机/分布式的数据
      for (let i = 0; i < data.length; i++) {
        let date = data[i].date;
        tmp_option.push(date);
        tmp_data[date] = data[i];
      }
      this.legend = ['G', 'S', 'B'];
      this.title = this.tabName;
      this.option = tmp_option;
      this.datas = tmp_data;
    }
  }
};
</script>

<style scoped>
</style>
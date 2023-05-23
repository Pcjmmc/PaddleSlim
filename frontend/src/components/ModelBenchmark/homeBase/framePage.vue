<template>
  <div style="margin-top:1%;">
    <el-tabs
      v-model="tabName"
      type="card"
      @tab-click="clickTab"
    >
      <el-tab-pane
        label="Paddle模型数"
        name="paddle"
      >
      </el-tab-pane>
      <el-tab-pane
        label="竞品模型数"
        name="pytorch"
      >
      </el-tab-pane>
      <frame-statistics :datas="datas"></frame-statistics>
    </el-tabs>
  </div>
</template>
<script>

import frameStatistics from './frameStatistics.vue';
import api from '../../../api/index';
import { ModelsBenchmarkHomeDraw } from '../../../api/url.js';

export default {
  name: 'framePage',
  data: function () {
    return {
      tabName: 'paddle',
      datas: {
        pie: {
          option: [],
          datas: []
        },
        colum: {
          option: [],
          datas: {}
        }
      }
    };
  },
  watch: {
  },
  mounted: function () {
    this.getDatas();
  },
  components: {
    frameStatistics
  },
  computed: {},
  methods: {
    clickTab(name) {
      this.tabName = name.name;
      this.datas = {
        pie: {
          option: [],
          datas: []
        },
        colum: {
          option: [],
          datas: {}
        }
      };
      this.getDatas();
    },
    async getDatas() {
      let params = {
        frame: this.tabName
      };
      const { code, data, message } = await api.post(ModelsBenchmarkHomeDraw, params);
      if (parseInt(code, 10) === 200) {
        this.prepareDatas(data);
      } else {
        this.$Message.error({
            content: '请求出错: ' + message,
            duration: 30,
            closable: true
        });
      }
    },
    prepareDatas(data) {
      let temp = data[this.tabName];
      let pie_datas = [];
      let colum_datas = {};
      let opt = [];
      for (let i = 0; i < temp.length; i++) {
        for (let key in temp[i]) {
          if (temp[i].hasOwnProperty(key)) {
            opt.push(key);
            let tmp = {
              value: temp[i][key].total_num,
              name: key
            };
            pie_datas.push(tmp);
            colum_datas[key] = temp[i][key];
          }
        }
      }
      this.datas.pie.datas = pie_datas;
      this.datas.pie.option = opt;
      this.datas.colum.datas = colum_datas;
      this.datas.colum.option = opt;
    }
  }
};
</script>

<style scoped>
</style>
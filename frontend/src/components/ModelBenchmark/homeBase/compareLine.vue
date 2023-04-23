<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div :id="id" style="height: 350px;"></div>
</template>
<script>
import echarts from 'echarts';
require('echarts/lib/chart/line');
require('echarts/lib/component/tooltip');
require('echarts/lib/component/title');
require('echarts/lib/component/legend');
export default {
  name: 'compareLine',
  props: {
    option: {
      type: Array,
      default: function () {
        return [];
      }
    },
    id: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
    optionData: {
      type: Object,
      default: function () {
        return {};
      }
    },
    legend: {
      type: Array,
      default: function () {
        return [];
      }
    }
  },
  data() {
    return {
      charts: ''
    };
  },
  watch: {
    // 观察option的变化
    optionData: function () {
      console.log('change', this.id);
      this.$nextTick(function () {
        this.drawPie(this.id);
      });
    }
  },
  methods: {
    getSeirse() {
      let res = {};
      let result = [];
      for (let j in this.legend) {
        res[this.legend[j]] = {
          name: this.legend[j],
          data: [],
          type: 'line'
        };
      }
      for (let i in this.legend) {
        for (let k in this.option) {
          let obj = this.optionData[this.option[k]];
          res[this.legend[i]].data.push(obj[this.legend[i]]);
        }
      }
      for (let v in res) {
        result.push(res[v]);
      }
      return result;
    },
    drawPie(id) {
      this.charts = echarts.init(document.getElementById(id));
      this.charts.setOption(
        {
          legend: {
            data: this.legend
          },
          xAxis: {
            type: 'category',
            data: this.option,
            name: '日期',
            // x轴名称样式
            nameTextStyle: {
              fontWeight: 600,
              fontSize: 18
            }
          },
          yAxis: {
            type: 'value',
            name: '数量',
            // y轴名称样式
            nameTextStyle: {
              fontWeight: 600,
              fontSize: 18
            }
          },
          tooltip: {
            trigger: 'axis'
          },
          series: this.getSeirse()
        }, true
      );
    }
  },
  mounted() {
    this.$nextTick(function () {
      this.drawPie(this.id);
    });
  }
};
</script>
<style scoped>
  * {
    margin: 0;
    padding: 0;
    list-style: none;
  }
</style>
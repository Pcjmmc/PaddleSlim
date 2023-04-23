<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div id="main2" style="height: 350px;"></div>
</template>
<script>
import echarts from 'echarts';

export default {
  name: 'frameColumn',
  props: {
    option: {
      type: Array,
      default: function () {
        return [];
      }
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
    }
  },
  data() {
    return {
      charts: '',
      colors: ['#44cef6', '#3eedef'],
      types: ['FP32', 'FP16']
    };
  },
  watch: {
    // 观察option的变化
    optionData: function () {
      console.log('change main2');
      this.$nextTick(function () {
        this.drawPie('main2');
      });
    }
  },
  methods: {
    drawPie(id) {
      this.charts = echarts.init(document.getElementById(id));
      this.charts.setOption({
        title: {
          text: this.title,
          left: 'center'
        },
        xAxis: {
          type: 'value'
        },
        grid: {
          left: '10%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        yAxis: {
          type: 'category',
          data: this.option
        },
        legend: {
          left: 'center',
          top: 'bottom',
          orient: 'horizontal',
          itemGap: 20
        },
        series: this.getSeirse()
      });
    },
    getSeirse() {
      let res = {};
      let result = [];
      for (let j in this.types) {
        res[this.types[j]] = {
          name: this.types[j],
          data: [],
          type: 'bar',
          stack: 'x',
          color: this.colors[j],
          label: {
            normal: {
              show: true,
              formatter: '{c}'
            }
          }
        };
      }
      for (let k in this.option) {
        let obj = this.optionData[this.option[k]];
        for (let i in this.types) {
          res[this.types[i]].data.push(obj[this.types[i]]);
        }
      }
      for (let v in res) {
        result.push(res[v]);
      }
      return result;
    }
  },
  mounted() {
    this.$nextTick(function () {
      this.drawPie('main2');
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
<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div id="main1" style="height: 400px;"></div>
</template>
<script>
import echarts from 'echarts';
require('echarts/lib/chart/pie');
export default {
  name: 'framePie',
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
  // 在Chart.vue中加入watch
  watch: {
    // 观察option的变化
    optionData: function () {
      this.$nextTick(function () {
        this.drawPie('main1');
      });
    }
  },
  methods: {
    drawPie(id) {
      this.charts = echarts.init(document.getElementById(id));
      this.charts.setOption({
        graphic: {
          type: 'text',
          left: 'center',
          top: 'center',
          style: {
            // 数据总量
            textAlign: 'center',
            fill: 'black',
            fontSize: 30
          }
        },
        grid: {
          left: '10%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        title: {
          text: this.title,
          left: 'center'
        },
        legend: {
          orient: 'horizontal',
          bottom: 'bottom',
          left: '10',
          data: this.option,
          padding: [10, 0],
          type: 'scroll',
          itemWidth: 15,
          itemHeight: 15
        },
        series: [
          {
            type: 'pie',
            label: {
              normal: {
                show: true,
                formatter: '{b}: {c}'
              }
            },
            radius: '55%',
            center: ['50%', '50%'],
            labelLine: {
              show: true
            },
            data: this.optionData,
            emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
        ]
      });
    }
  },
  mounted() {
    this.$nextTick(function () {
      this.drawPie('main1');
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